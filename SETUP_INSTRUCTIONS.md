# RAG Model Setup Instructions

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Copy env file and configure:**
   ```bash
   cp env.example .env
   # then edit .env and fill in your values
   ```

   Required keys:
   - `HOST` (default `0.0.0.0`)
   - `PORT` (default `8000`)
   - `RELOAD` (default `true`)
   - `CORS_ALLOW_ORIGINS` (default `http://localhost:3000`)
   - `PINECONE_API_KEY` (required)
   - `PINECONE_INDEX_NAME` (required)
   - `PINECONE_ENVIRONMENT` (only for legacy client usage)
   - `OLLAMA_HOST` (default `http://localhost:11434`)

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python run.py
   ```
   
   The backend will start on `http://localhost:8000`

## Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will start on `http://localhost:3000`

## Testing the Integration

1. **Backend Health Check:**
   Visit `http://localhost:8000` - you should see `{"message": "RAG Model API is running!"}`

2. **Frontend Application:**
   Visit `http://localhost:3000` - you should see the RAG model interface

3. **File Upload Test:**
   - Upload a supported file (PDF, TXT, DOC, DOCX, CSV, JSON)
   - Check that the upload progress works
   - Verify the file appears in the files list

4. **Chat Test:**
   - Send a message in the chat interface
   - Verify you get a response from the backend

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Troubleshooting

- **CORS Issues:** Make sure both frontend (port 3000) and backend (port 8000) are running
- **File Upload Issues:** Check file size (max 10MB) and file type support
- **Connection Issues:** Verify the API_BASE_URL in frontend constants matches your backend URL
 - **Pinecone/Ollama Issues:** Ensure `.env` includes Pinecone keys and Ollama daemon is running with model `mxbai-embed-large` pulled (`ollama pull mxbai-embed-large`).


