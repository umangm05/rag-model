from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.files import router as files_router
from routes.chat import router as chat_router

app = FastAPI(
    title="RAG Model API",
    description="API for file upload and chat functionality",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "RAG Model API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}