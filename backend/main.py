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

    chunks = search(request.question)

    context = create_context(chunks)

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer
    }