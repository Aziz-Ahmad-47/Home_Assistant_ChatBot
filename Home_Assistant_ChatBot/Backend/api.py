from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.chat import ask_home_assistant


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Daily Home Management Assistant API",
    description="RAG-based household management chatbot API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):

    question: str


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Daily Home Management Assistant API is running",
        "status": "success"
    }


# =========================================================
# CHAT ENDPOINT
# =========================================================

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:

        return {
            "success": False,
            "answer": "Please enter a question."
        }

    try:

        answer = ask_home_assistant(question)

        return {
            "success": True,
            "question": question,
            "answer": answer
        }

    except Exception as error:

        return {
            "success": False,
            "answer": "Sorry, something went wrong.",
            "error": str(error)
        }