# RAG Model Backend API

A FastAPI-based backend for file upload and chat functionality.

## Features

- **File Upload**: Upload documents with progress tracking
- **File Management**: List and delete uploaded files
- **Chat API**: Send messages and get AI responses
- **CORS Support**: Configured for frontend integration

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables** (Optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Run the Server**
   ```bash
   # Option 1: Using the run script
   python run.py
   
   # Option 2: Using uvicorn directly
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Files
- `POST /api/v1/files/upload` - Upload a file
- `GET /api/v1/files` - List uploaded files
- `DELETE /api/v1/files/{file_id}` - Delete a file

### Chat
- `POST /api/v1/chat/message` - Send a chat message
- `GET /api/v1/chat/messages` - Get chat history

### Health
- `GET /` - API status
- `GET /health` - Health check

## File Upload

The API supports the following file types:
- PDF documents
- Text files
- Word documents (.doc, .docx)
- CSV files
- JSON files

Maximum file size: 10MB

## Development

The backend is structured with separate route files:
- `routes/files.py` - File upload and management
- `routes/chat.py` - Chat functionality
- `main.py` - FastAPI app configuration

Files are stored in the `uploads/` directory (created automatically).

