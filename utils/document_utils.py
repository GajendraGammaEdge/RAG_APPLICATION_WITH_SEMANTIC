from PyPDF2 import PdfReader
from io import BytesIO
import logging


def get_file_metadata(filename: str, content_type: str, file_bytes: bytes):
    doc_name = filename
    doc_type = filename.split(".")[-1].lower()
    doc_size = len(file_bytes)
    return doc_name, doc_type, doc_size


def extract_text_from_bytes(file_bytes: bytes, ext: str) -> str:
    text = ""

    if ext == "pdf":
        reader = PdfReader(BytesIO(file_bytes))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"

    elif ext in ["txt", "md"]:
        text = file_bytes.decode("utf-8")

    else:
        raise ValueError("Unsupported file type")

    return text


def extract_pages_with_numbers(file_bytes: bytes, ext: str):
    pages = []

    if ext == "pdf":
        reader = PdfReader(BytesIO(file_bytes))
        for idx, page in enumerate(reader.pages):
            pages.append({
                "page_number": idx + 1,
                "text": page.extract_text() or ""
            })

    elif ext in ["txt", "md"]:
        pages.append({
            "page_number": 1,
            "text": file_bytes.decode("utf-8")
        })

    else:
        raise ValueError("Unsupported file type")

    return pages


def chunk_text(text, chunk_size=500, overlap=50):
    logging.info("Chunking started")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    logging.info(f"Created {len(chunks)} chunks")
    return chunks