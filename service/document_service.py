from sqlalchemy.orm import Session
from db_configuration.pgdb_config import SessionLocal
from schema.document_metadata import DocumentMetadata
from schema.documents_chunks import DocumentChunks
from utils.document_utils import (
    get_file_metadata,
    extract_text_from_bytes,
    chunk_text,
)
from utils.embedding_utils import get_embedding
import logging


class DocumentService:

    @staticmethod
    def upload_document(
        user_id: int,
        file_bytes: bytes,
        filename: str,
        content_type: str
    ):
        db: Session = SessionLocal()

        try:
            doc_name, doc_type, doc_size = get_file_metadata(
                filename,
                content_type,
                file_bytes
            )

            document = DocumentMetadata(
                doc_name=doc_name,
                doc_type=doc_type,
                doc_size=doc_size,
                file_data=file_bytes,
                user_id=user_id
            )

            db.add(document)
            db.commit()
            db.refresh(document)

            text = extract_text_from_bytes(file_bytes, doc_type)
            print(f"text_pypdf2 {text}")
            chunks = chunk_text(text)

            for chunk in chunks:
                embedding_vector = get_embedding(chunk)
                db.add(
                    DocumentChunks(
                        doc_id=document.doc_id,
                        content=chunk,
                        embedding=embedding_vector
                    )
                )

            db.commit()
            logging.info(f"Document processed successfully for user {user_id}")

        except Exception:
            db.rollback()
            logging.exception("Background document upload failed")

        finally:
            db.close()
