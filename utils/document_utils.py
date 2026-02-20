
from PyPDF2 import PdfReader
import logging
from PyPDF2 import PdfReader
from io import BytesIO


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


def chunk_text(text, chunk_size=500, overlap=50):
    logging.info(f"chunking of the data is started")
    words = text.split()
    chunks = []
    start = 0
    logging.debug(f"chunking of the file is started")
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
