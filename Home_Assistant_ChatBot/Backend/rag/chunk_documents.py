from langchain_text_splitters import RecursiveCharacterTextSplitter

from load_documents import load_pdf_documents


def create_chunks():

    # Load PDFs
    documents = load_pdf_documents()

    # Text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    all_chunks = []

    for document in documents:

        text = document["text"]
        source = document["source"]

        chunks = text_splitter.split_text(text)

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "source": source,
                "chunk_id": index + 1,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()

    print("\n" + "=" * 60)
    print("TEXT CHUNKING COMPLETED")
    print("=" * 60)

    print(f"\nTotal chunks created: {len(chunks)}")

    for chunk in chunks[:5]:

        print("\n" + "-" * 60)

        print(
            f"Source: {chunk['source']}"
        )

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )

        print("\nText:")

        print(chunk["text"])