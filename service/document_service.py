from sqlalchemy.orm import Session
from db_configuration.pgdb_config import SessionLocal
from schema.document_metadata import DocumentMetadata
from schema.documents_chunks import DocumentChunks
from schema.document_page import DocumentPages
from utils.document_utils import (
    get_file_metadata,
    extract_text_from_bytes,
    chunk_text,
    extract_pages_with_numbers,  
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

            pages = extract_pages_with_numbers(file_bytes, doc_type)

            for page in pages:
                db.add(
                    DocumentPages(
                        doc_id=document.doc_id,
                        page_number=page["page_number"],
                        content=page["text"]
                    )
                )

            full_text = extract_text_from_bytes(file_bytes, doc_type)
            chunks = chunk_text(full_text)

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
            logging.info(
                f"Document processed successfully (doc_id={document.doc_id})"
            )

        except Exception as e:
            db.rollback()
            logging.exception(
                f"Document upload failed for user {user_id}: {str(e)}"
            )
            raise

        finally:
            db.close()