from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ExamPrep AI",
    version="1.0.0",
    description="AI-powered Exam Preparation Assistant"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home Route
@app.get("/")
def home():
    return {
        "message": "Welcome to ExamPrep AI 🚀"
    }


# Health Check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Build Knowledge Base
@app.post("/build-db")
def build_db():

    # Lazy import so the embedding model loads only when needed
    from embeddings import build_database

    total_chunks = build_database()

    return {
        "message": "Knowledge Base Created Successfully",
        "chunks": total_chunks
    }