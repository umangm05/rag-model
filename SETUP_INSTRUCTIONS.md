# RAG Model Setup Instructions

## Quick Start with Docker (Recommended)

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - Pinecone API key and index name

2. **Setup environment:**
   ```bash
   # Copy the Docker environment template
   cp env.docker .env
   
   # Edit .env and add your Pinecone credentials
   # PINECONE_API_KEY=your_actual_api_key
   # PINECONE_INDEX_NAME=your_actual_index_name
   ```

3. **Start everything with one command:**
   ```bash
   make start
   # or manually:
   # docker-compose build
   # docker-compose up -d
   # ./scripts/setup-ollama.sh
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - RabbitMQ Management: http://localhost:15672 (guest/guest)

5. **Useful commands:**
   ```bash
   make logs          # View all logs
   make status        # Check service status
   make down          # Stop all services
   make clean         # Remove everything
   ```

## Manual Setup (Alternative)

### Backend Setup

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
   - `RABBITMQ_URL` (default `amqp://guest:guest@localhost:5672/`)
   - `RABBITMQ_QUEUE_NAME` (default `file_processing_queue`)
   - `REDIS_URL` (default `redis://localhost:6379/0`)

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start required services:**
   
   **RabbitMQ (for file processing queue):**
   ```bash
   # Using Docker (recommended)
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   
   # Or install locally and start service
   # macOS: brew install rabbitmq && brew services start rabbitmq
   # Ubuntu: sudo apt install rabbitmq-server && sudo systemctl start rabbitmq-server
   ```
   
   **Redis (for Celery result backend):**
   ```bash
   # Using Docker (recommended)
   docker run -d --name redis -p 6379:6379 redis:alpine
   
   # Or install locally and start service
   # macOS: brew install redis && brew services start redis
   # Ubuntu: sudo apt install redis-server && sudo systemctl start redis-server
   ```
   
   **Ollama (for embeddings):**
   ```bash
   # Install Ollama and pull the embedding model
   ollama pull mxbai-embed-large
   ```

5. **Start the backend server:**
   ```bash
   python run.py
   ```
   
   The backend will start on `http://localhost:8000`

6. **Start the file processing consumer (in a separate terminal):**
   ```bash
   python consumer.py
   ```
   
   This will start consuming file processing tasks from RabbitMQ

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

### Docker Setup Issues
- **Docker not starting:** Ensure Docker Desktop is running and you have sufficient resources allocated
- **Port conflicts:** Make sure ports 3000, 8000, 5672, 6379, 11434, and 15672 are not in use
- **Build failures:** Try `docker-compose build --no-cache` to rebuild from scratch
- **Service health checks failing:** Check logs with `make logs` or `docker-compose logs [service-name]`

### Application Issues
- **CORS Issues:** Make sure both frontend (port 3000) and backend (port 8000) are running
- **File Upload Issues:** Check file size (max 10MB) and file type support
- **Connection Issues:** Verify the API_BASE_URL in frontend constants matches your backend URL
- **Pinecone/Ollama Issues:** Ensure `.env` includes Pinecone keys and Ollama model is pulled
- **RabbitMQ Issues:** Check RabbitMQ management UI at `http://localhost:15672` (guest/guest)
- **Redis Issues:** Ensure Redis is running and accessible
- **File Processing Issues:** Check consumer logs with `make logs-consumer`
- **Status Updates:** The UI polls for status updates every 2 seconds. If files appear stuck, check the consumer logs

### Docker Commands
```bash
# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f consumer
docker-compose logs -f frontend

# Restart specific service
docker-compose restart backend
docker-compose restart consumer

# Check service status
docker-compose ps

# Access service shell
docker-compose exec backend bash
docker-compose exec consumer bash
```


