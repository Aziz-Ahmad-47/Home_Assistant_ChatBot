from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# FAISS database location
DB_DIR = Path(__file__).parent.parent / "vector_db"


# Same embedding model used while creating the database
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load existing FAISS database
vector_db = FAISS.load_local(
    str(DB_DIR),
    embeddings,
    allow_dangerous_deserialization=True
)


def search_documents(question, number_of_results=4):

    results = vector_db.similarity_search(
        question,
        k=number_of_results
    )

    return results


if __name__ == "__main__":

    question = input(
        "\nAsk a question about your household: "
    )

    results = search_documents(question)

    print("\n" + "=" * 60)
    print("RELEVANT INFORMATION")
    print("=" * 60)

    for index, document in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("-" * 60)

        print(
            f"Source: {document.metadata.get('source', 'Unknown')}"
        )

        print(
            f"Chunk: {document.metadata.get('chunk_id', 'Unknown')}"
        )

        print("\nContent:")
        print(document.page_content)