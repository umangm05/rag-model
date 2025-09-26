# RAG Model - Full-Stack Retrieval-Augmented Generation System

A comprehensive RAG (Retrieval-Augmented Generation) application built with Next.js frontend, Python FastAPI backend, and Docker Compose orchestration.

## 🚀 Features

- **Modern Frontend**: Next.js with TypeScript and Tailwind CSS
- **Powerful Backend**: Python FastAPI with comprehensive RAG functionality
- **Document Processing**: Support for PDF, DOCX, and TXT files
- **Vector Database**: ChromaDB for efficient document retrieval
- **AI Integration**: OpenAI GPT integration for enhanced responses
- **Containerized**: Complete Docker Compose setup for easy deployment
- **Chat Interface**: Real-time chat interface for document Q&A

## 📁 Project Structure

```
rag-model/
├── frontend/                 # Next.js Frontend Application
│   ├── src/
│   │   └── app/
│   │       └── page.tsx      # Main chat interface
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.js
├── backend/                  # Python FastAPI Backend
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configuration
│   │   ├── models/           # Pydantic models
│   │   └── services/         # Business logic
│   ├── data/                 # Persistent data storage
│   │   ├── uploads/          # Uploaded documents
│   │   └── chroma/           # Vector database
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml        # Docker orchestration
├── .env.example             # Environment configuration template
└── README.md                # This file
```

## 🛠️ Prerequisites

- Docker and Docker Compose
- OpenAI API key (required for RAG functionality)
- Git

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd rag-model
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env
cp backend/.env.example backend/.env

# Edit .env files and add your OpenAI API key
# Required: OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Development Setup (Optional)

If you want to run services individually for development:

#### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 📚 Usage

### 1. Document Upload
- Navigate to the chat interface at http://localhost:3000
- Use the backend API at http://localhost:8000/docs to upload documents
- Supported formats: PDF, DOCX, TXT

### 2. Chat Interface
- Ask questions about your uploaded documents
- The system will retrieve relevant information and provide AI-enhanced responses
- View source references for transparency

### 3. API Endpoints

- `POST /api/chat` - Send chat messages
- `POST /api/upload` - Upload documents
- `GET /api/documents` - List uploaded documents
- `DELETE /api/documents/{id}` - Delete documents
- `GET /health` - Health check

## 🔧 Configuration

### Backend Configuration

The backend can be configured via environment variables in `backend/.env`:

```env
# Application Settings
ENVIRONMENT=development

# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RETRIEVAL_RESULTS=5
MAX_FILE_SIZE=10485760  # 10MB

# Database
CHROMA_PERSIST_DIRECTORY=./data/chroma
```

### Frontend Configuration

The frontend automatically proxies API requests to the backend service when running in Docker.

## 🐳 Docker Commands

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Run in production mode
docker-compose -f docker-compose.yml up --build -d
```

## 📝 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

## 🔍 Troubleshooting

### Common Issues

1. **"RAG service not properly configured"**
   - Ensure your OpenAI API key is set in the environment variables
   - Check the backend logs: `docker-compose logs backend`

2. **Frontend can't connect to backend**
   - Ensure both services are running
   - Check Docker network connectivity
   - Verify the backend is healthy: http://localhost:8000/health

3. **Document upload fails**
   - Check file size limits (default: 10MB)
   - Ensure supported file format (PDF, DOCX, TXT)
   - Check backend logs for detailed errors

### Development Tips

- Use `docker-compose logs -f [service-name]` to view real-time logs
- Backend auto-reloads in development mode
- Frontend supports hot-reloading during development
- Vector database persists data in `backend/data/chroma`

## 🛡️ Security Notes

- Never commit `.env` files with real API keys
- The vector database and uploaded files persist in Docker volumes
- Use environment-specific configurations for production deployments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker Compose
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Next.js, FastAPI, and Docker**

