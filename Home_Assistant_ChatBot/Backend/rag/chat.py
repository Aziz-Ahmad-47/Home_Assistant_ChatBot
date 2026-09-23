import os
from pathlib import Path

import streamlit as st
from groq import Groq

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# =========================================================
# CONFIGURATION
# =========================================================

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured")

MODEL = "openai/gpt-oss-20b"

DB_DIR = Path(__file__).parent.parent / "vector_db"


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# LOAD VECTOR DATABASE
# =========================================================

print("Loading FAISS vector database...")

vector_db = FAISS.load_local(
    str(DB_DIR),
    embeddings,
    allow_dangerous_deserialization=True
)


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# RAG CHAT FUNCTION
# =========================================================

def ask_home_assistant(question):

    # ---------------------------------------------
    # 1. Search relevant documents
    # ---------------------------------------------

    documents = vector_db.similarity_search(
        question,
        k=4
    )

    if not documents:
        return "I could not find relevant information in the household documents."


    # ---------------------------------------------
    # 2. Prepare context
    # ---------------------------------------------

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"{document.page_content}"
        )

    context = "\n\n".join(context_parts)


    # ---------------------------------------------
    # 3. Create prompt
    # ---------------------------------------------

    prompt = f"""
You are a helpful Daily Home Management Assistant.

Answer the user's question using the provided household documents.

Rules:

Rules:

1. Use the household documents whenever possible.
2. Do not invent household information.
3. If the requested information is not available, clearly say that it is not available.
4. Give a clear and concise answer.
5. When useful, mention the source PDF.
6. Do not mention technical terms such as RAG, FAISS, embeddings, or vector database.
7. Answer naturally like a helpful family assistant.
8. NEVER use Hindi or Devanagari script.
9. If the user asks in English, answer in English.
10. If the user asks in Urdu, answer in Urdu script.
11. If the user asks in Roman Urdu, answer in Roman Urdu.
12. If the user mixes English and Roman Urdu, respond in the same mixed style.
13. If the user asks you to CREATE, PLAN, SUGGEST, ESTIMATE, or CALCULATE something using information provided in the question, you may generate a practical response without requiring that information to exist in the PDF documents.
14. For budgeting requests, use the user's provided income, family size, month, and other details to create a reasonable suggested budget.
15. Clearly label estimated or suggested amounts as estimates. Do not present them as actual household expenses.
16. Use PDF data when the user asks about actual historical household expenses, bills, groceries, or tasks.
17. If the user asks for a future plan such as a monthly budget, grocery plan, savings plan, or task plan, create the plan using the information provided by the user.
18. Never say that information is unavailable merely because the requested future plan is not present in the PDF documents.

HOUSEHOLD DOCUMENTS:

{context}


USER QUESTION:

{question}
"""


    # ---------------------------------------------
    # 4. Send request to Groq
    # ---------------------------------------------

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a reliable Daily Home Management Assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )


    # ---------------------------------------------
    # 5. Return answer
    # ---------------------------------------------

    return response.choices[0].message.content


# =========================================================
# TEST CHATBOT
# =========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("DAILY HOME MANAGEMENT ASSISTANT")
    print("=" * 60)

    question = input("\nAsk your Home Assistant: ")

    answer = ask_home_assistant(question)

    print("\nAssistant:")
    print("-" * 60)
    print(answer)
