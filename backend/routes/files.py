import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import shutil
import logging
from services.queue_service import queue_service
from services.status_service import status_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/files", tags=["files"])

# Directory to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory storage for file metadata (in production, use a database)
uploaded_files_db = {}

# File type validation
ALLOWED_TYPES = [
    'application/pdf',
    'text/plain',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/csv',
    'application/json',
]

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile):
    """Validate uploaded file"""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not supported. Allowed types: {', '.join(ALLOWED_TYPES)}"
        )
    
    # Note: file.size might not be available in all cases
    # For production, you might want to check size during upload

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the server"""
    try:
        # Validate file
        validate_file(file)
        
        # Generate unique file ID and filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size after saving
        file_size = os.path.getsize(file_path)
        
        # Check file size after upload
        if file_size > MAX_FILE_SIZE:
            os.remove(file_path)  # Clean up
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {MAX_FILE_SIZE / (1024 * 1024)}MB limit"
            )
        
        # Store file metadata
        file_metadata = {
            "id": file_id,
            "name": file.filename,
            "size": file_size,
            "type": file.content_type,
            "uploadedAt": datetime.now().isoformat(),
            "status": "uploaded",
            "progress": 0,
            "path": file_path
        }
        
        uploaded_files_db[file_id] = file_metadata
        
        # Initialize status tracking
        status_service.update_file_status(
            file_id=file_id,
            status="uploaded",
            progress=0,
            message="File uploaded successfully"
        )
        
        # Enqueue file for processing
        try:
            queue_data = {
                "file_id": file_id,
                "file_path": file_path,
                "file_name": file.filename,
                "file_type": file.content_type,
                "file_size": file_size
            }
            
            success = queue_service.publish_file_processing_task(queue_data)
            if success:
                status_service.update_file_status(
                    file_id=file_id,
                    status="queued",
                    progress=5,
                    message="File queued for processing"
                )
                logger.info(f"File {file.filename} queued for processing")
            else:
                status_service.update_file_status(
                    file_id=file_id,
                    status="failed",
                    progress=0,
                    message="Failed to queue file for processing",
                    error="Queue service unavailable"
                )
                logger.error(f"Failed to queue file {file.filename} for processing")
                
        except Exception as e:
            logger.error(f"Error queuing file {file.filename}: {e}")
            status_service.update_file_status(
                file_id=file_id,
                status="failed",
                progress=0,
                message="Failed to queue file for processing",
                error=str(e)
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "file": {
                    "id": file_metadata["id"],
                    "name": file_metadata["name"],
                    "size": file_metadata["size"],
                    "type": file_metadata["type"],
                    "uploadedAt": file_metadata["uploadedAt"],
                    "status": file_metadata["status"],
                    "progress": file_metadata["progress"]
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("")
async def get_files():
    """Get list of uploaded files with current processing status"""
    files = []
    for file_data in uploaded_files_db.values():
        file_id = file_data["id"]
        
        # Get current status from status service
        status_info = status_service.get_file_status(file_id)
        
        file_info = {
            "id": file_data["id"],
            "name": file_data["name"],
            "size": file_data["size"],
            "type": file_data["type"],
            "uploadedAt": file_data["uploadedAt"],
            "status": status_info.get("status", "unknown") if status_info else "unknown",
            "progress": status_info.get("progress", 0) if status_info else 0,
            "message": status_info.get("message", "") if status_info else "",
            "error": status_info.get("error") if status_info else None
        }
        files.append(file_info)
    
    return {"files": files}

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file"""
    if file_id not in uploaded_files_db:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Get file metadata
        file_data = uploaded_files_db[file_id]
        
        # Delete file from disk
        if os.path.exists(file_data["path"]):
            os.remove(file_data["path"])
        
        # Remove from database
        del uploaded_files_db[file_id]
        
        # Remove from status tracking
        status_service.delete_file_status(file_id)
        
        return {"message": "File deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@router.get("/{file_id}/status")
async def get_file_status(file_id: str):
    """Get the current processing status of a specific file"""
    if file_id not in uploaded_files_db:
        raise HTTPException(status_code=404, detail="File not found")
    
    status_info = status_service.get_file_status(file_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="Status not found for file")
    
    return {
        "file_id": file_id,
        "status": status_info["status"],
        "progress": status_info["progress"],
        "message": status_info["message"],
        "error": status_info.get("error"),
        "updated_at": status_info["updated_at"]
    }

@router.get("/status/all")
async def get_all_file_statuses():
    """Get processing status of all files"""
    all_statuses = status_service.get_all_file_statuses()
    return {"statuses": all_statuses}


