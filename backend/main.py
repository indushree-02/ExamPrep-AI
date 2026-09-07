from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from embeddings import build_database
from retriever import search
from generator import generate_answer, create_context


app = FastAPI(
    title="ExamPrep AI",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "ExamPrep AI Backend Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/build-db")
def build_db():

    total_chunks = build_database()

    return {
        "message": "Knowledge Base Created Successfully",
        "chunks": total_chunks
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    # Retrieve relevant documents and their metadata
    documents, metadatas = search(request.question)

    # Create context for the LLM
    context = create_context(documents)

    # Generate answer
    answer = generate_answer(
        request.question,
        context
    )

    # Get unique source filenames
    sources = []

    for metadata in metadatas:

        source = metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }