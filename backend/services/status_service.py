import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StatusService:
    """Service to track file processing status"""
    
    def __init__(self):
        # In-memory storage for file statuses
        # In production, this should be a database (Redis, PostgreSQL, etc.)
        self.file_statuses: Dict[str, Dict[str, Any]] = {}
    
    def update_file_status(self, file_id: str, status: str, progress: int = None, 
                          message: str = None, error: str = None) -> None:
        """
        Update the processing status of a file
        
        Args:
            file_id: Unique file identifier
            status: Current status (uploaded, queued, processing, embedding, completed, failed)
            progress: Progress percentage (0-100)
            message: Status message
            error: Error message if failed
        """
        if file_id not in self.file_statuses:
            self.file_statuses[file_id] = {
                "file_id": file_id,
                "status": "uploaded",
                "progress": 0,
                "message": "File uploaded successfully",
                "error": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        
        # Update status
        self.file_statuses[file_id]["status"] = status
        self.file_statuses[file_id]["updated_at"] = datetime.now().isoformat()
        
        if progress is not None:
            self.file_statuses[file_id]["progress"] = progress
        
        if message is not None:
            self.file_statuses[file_id]["message"] = message
        
        if error is not None:
            self.file_statuses[file_id]["error"] = error
        
        logger.info(f"Updated status for file {file_id}: {status} ({progress}%)")
    
    def get_file_status(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a file"""
        return self.file_statuses.get(file_id)
    
    def get_all_file_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all files"""
        return self.file_statuses
    
    def delete_file_status(self, file_id: str) -> bool:
        """Delete status record for a file"""
        if file_id in self.file_statuses:
            del self.file_statuses[file_id]
            return True
        return False

# Global status service instance
status_service = StatusService()

