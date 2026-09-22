from pathlib import Path
from pypdf import PdfReader


# PDF files ka folder
DATA_DIR = Path(__file__).parent.parent / "data"


def load_pdf_documents():

    documents = []

    # data folder ke andar tamam PDF files
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {DATA_DIR}"
        )

    for pdf_file in pdf_files:

        print(f"\nLoading: {pdf_file.name}")

        reader = PdfReader(str(pdf_file))

        full_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                full_text += text + "\n"

        documents.append({
            "source": pdf_file.name,
            "text": full_text
        })

        print(
            f"Pages: {len(reader.pages)}"
        )

        print(
            f"Characters extracted: {len(full_text)}"
        )

    return documents


if __name__ == "__main__":

    documents = load_pdf_documents()

    print("\n" + "=" * 60)
    print("PDF LOADING COMPLETED")
    print("=" * 60)

    for document in documents:

        print(
            f"\nSource: {document['source']}"
        )

        print(
            document["text"][:500]
        )

        print("\n" + "-" * 60)