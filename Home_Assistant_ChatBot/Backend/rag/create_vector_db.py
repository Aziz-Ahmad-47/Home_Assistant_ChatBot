from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from chunk_documents import create_chunks


# Vector database ka folder
DB_DIR = Path(__file__).parent.parent / "vector_db"


def create_vector_database():

    print("\nLoading and chunking PDF documents...")

    chunks = create_chunks()

    if not chunks:
        raise ValueError("No chunks were created from the PDF files.")

    # Convert chunks into LangChain Documents
    documents = []

    for chunk in chunks:

        document = Document(
            page_content=chunk["text"],
            metadata={
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
            }
        )

        documents.append(document)

    print(f"Total documents/chunks: {len(documents)}")

    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating embeddings...")

    vector_db = FAISS.from_documents(
        documents,
        embeddings
    )

    # Vector database folder create
    DB_DIR.mkdir(exist_ok=True)

    print("\nSaving FAISS vector database...")

    vector_db.save_local(str(DB_DIR))

    print("\n" + "=" * 60)
    print("VECTOR DATABASE CREATED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nLocation: {DB_DIR}")
    print(f"Total vectors: {len(documents)}")


if __name__ == "__main__":
    create_vector_database()