from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# In-memory storage for chat messages (in production, use a database)
chat_messages_db: List[Dict] = [
    {
        "id": "1",
        "content": "Hello! I'm here to help you with your uploaded documents. Upload some files and ask me questions about them!",
        "timestamp": datetime.now().isoformat(),
        "isUser": False,
    }
]

class ChatMessageRequest(BaseModel):
    content: str

class ChatMessageResponse(BaseModel):
    id: str
    content: str
    timestamp: str
    isUser: bool

MAX_MESSAGE_LENGTH = 1000

@router.post("/message")
async def send_message(message_request: ChatMessageRequest):
    """Send a chat message and get AI response"""
    try:
        content = message_request.content.strip()
        
        # Validate message length
        if len(content) > MAX_MESSAGE_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Message exceeds {MAX_MESSAGE_LENGTH} character limit"
            )
        
        if not content:
            raise HTTPException(status_code=400, detail="Message content cannot be empty")
        
        # Create user message
        user_message = {
            "id": f"msg_{len(chat_messages_db) + 1}_user",
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "isUser": True,
        }
        
        chat_messages_db.append(user_message)
        
        # Generate AI response (mock for now)
        ai_response_content = generate_ai_response(content)
        ai_message = {
            "id": f"msg_{len(chat_messages_db) + 1}_ai",
            "content": ai_response_content,
            "timestamp": datetime.now().isoformat(),
            "isUser": False,
        }
        
        chat_messages_db.append(ai_message)
        
        return {
            "message": "Message sent successfully",
            "response": ai_message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.get("/messages")
async def get_messages():
    """Get all chat messages"""
    return {"messages": chat_messages_db}

def generate_ai_response(user_message: str) -> str:
    """Generate a mock AI response based on user message"""
    lower_message = user_message.lower()
    
    # Import here to avoid circular imports
    from .files import uploaded_files_db
    files_count = len(uploaded_files_db)
    
    if files_count == 0:
        return "I don't see any uploaded files yet. Please upload some documents first, and then I can help you analyze them!"
    
    if any(word in lower_message for word in ['hello', 'hi', 'hey']):
        return f"Hello! I can see you have {files_count} file(s) uploaded. How can I help you analyze them?"
    
    if any(word in lower_message for word in ['file', 'document']):
        file_names = [file_data["name"] for file_data in uploaded_files_db.values()]
        file_list = ", ".join(file_names)
        return f"You have uploaded the following files: {file_list}. What would you like to know about them?"
    
    if any(word in lower_message for word in ['summary', 'summarize']):
        return f"I'd be happy to summarize your documents! Based on the {files_count} file(s) you've uploaded, I can provide insights and key points. (This is a mock response - in the real implementation, I would analyze the actual content of your files.)"
    
    if any(word in lower_message for word in ['search', 'find']):
        return "I can help you search through your uploaded documents. What specific information are you looking for? (This is a mock response - in the real implementation, I would perform semantic search across your files.)"
    
    # Default responses
    responses = [
        f"That's an interesting question about your {files_count} uploaded file(s). Let me analyze them for you... (This is a mock response)",
        f"Based on your uploaded documents, here's what I found... (This is a mock response - real implementation would analyze actual file content)",
        f"I can help you with that! Your uploaded files contain relevant information. (This is a mock response)",
        f"Great question! I'm analyzing your documents to provide the best answer... (This is a mock response)",
    ]
    
    import random
    return random.choice(responses)


