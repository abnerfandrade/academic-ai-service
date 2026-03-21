import os
import hashlib

from loguru import logger
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    Form,
    File,
    HTTPException,
    UploadFile,
    status,
    Query
)

from src.repositories.document import DocumentRepository, DocumentCreate, DocumentFilters
from src.routes.documents.datatypes import DocumentResponse, UploadResponse
from src.routes.documents.service import run_rag_pipeline
from src.services.rag_pipeline import RagPipeline
from src.core.config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

SUPPORTED_EXTENSIONS = {
    ".pdf": "PDF",
}


def init_app(app: FastAPI) -> None:
    app.include_router(router)


@router.post("/upload", response_model=UploadResponse, status_code=202)
async def upload_documents(
    background_tasks: BackgroundTasks,
    class_name: str = Form(..., description="O nome da aula a qual o documento pertence"),
    file: UploadFile = File(...),
    rag_pipeline: RagPipeline = Depends(),
    doc_repo: DocumentRepository = Depends(),
) -> UploadResponse:
    try:
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

        filename = file.filename or "unknown"
        ext = os.path.splitext(filename)[1].lower()

        if ext not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Extensão '{ext}' não suportada. Suportadas: {', '.join(SUPPORTED_EXTENSIONS.keys())}",
            )

        content = await file.read()
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail=f"Arquivo '{filename}' excede o limite de {settings.MAX_UPLOAD_SIZE_MB}MB.",
            )

        filehash = hashlib.sha256(content).hexdigest()
        existing = await doc_repo.get_by_hash(filehash)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Arquivo com o mesmo conteúdo já foi enviado (filename='{existing.filename}').",
            )

        doc_data = DocumentCreate(
            class_name=class_name,
            filename=filename,
            filehash=filehash,
            status="queued"
        )
        doc_record = await doc_repo.create(doc_data, commit=True)
        document_id = doc_record.id

        logger.bind(filename=filename, size_bytes=len(content), document_id=str(document_id)).info("Arquivo aceito")

        file_data = {"filename": filename, "content": content}
        background_tasks.add_task(run_rag_pipeline, rag_pipeline, document_id, file_data)

        return UploadResponse(
            id=document_id,
            class_name=class_name,
            filename=filename,
            status="queued"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o arquivo: {str(e)}"
        )


@router.get("/{document_id}/status")
async def get_document_status(
    document_id: int,
    doc_repo: DocumentRepository = Depends(),
) -> dict:
    doc = await doc_repo.get_by_id(document_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )

    return {"status": doc.status}


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    id: int | None = Query(None, description="Filtrar pelo id do documento"),
    class_name: str | None = Query(None, description="Filtrar por nome da aula"),
    filename: str | None = Query(None, description="Filtrar por nome do documento"),
    doc_status: str | None = Query(None, description="Filtrar por status"),
    created_after: str | None = Query(None, description="Filtrar por data de criação após"),
    created_before: str | None = Query(None, description="Filtrar por data de criação antes"),
    doc_repo: DocumentRepository = Depends(),
) -> list[DocumentResponse]:
    try:
        filters = DocumentFilters(
            id=id,
            class_name=class_name,
            filename=filename,
            status=doc_status,
            created_after=created_after,
            created_before=created_before,
        )

        documents = await doc_repo.get_all(filters)

        return [
            DocumentResponse(
                id=doc.id,
                class_name=doc.class_name,
                filename=doc.filename,
                filehash=doc.filehash,
                status=doc.status,
                error_detail=doc.error_detail,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
            for doc in documents
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar documentos: {str(e)}"
        )
