# router/document_router.py
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    BackgroundTasks,
    HTTPException,
)
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db
from service.document_service import DocumentService
from utils.security import get_current_user
from schema.user_detailed import UserDetails

MAX_SIZE = 20 * 1024 * 1024
MAX_NUMBER_OF_DOCUMENT = 10 
router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    background_task: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: UserDetails = Depends(get_current_user),
): 
    if len(file) > MAX_NUMBER_OF_DOCUMENT:
         raise HTTPException(
              status_code=401,
              detail= f"You can only upload {MAX_NUMBER_OF_DOCUMENT} in once.Try remove few document"
         ) 
    file_bytes = await file.read()
    if len(file_bytes) > MAX_SIZE :
         raise HTTPException(
              status_code=413,
              detail= f"You need to upload the document less then {MAX_SIZE}"
         )
    service = DocumentService()

    background_task.add_task(
        service.upload_document,
        current_user.id,
        file_bytes,
        file.filename,
        file.content_type
    )

    return "Document uploaded successfully"
