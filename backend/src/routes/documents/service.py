from loguru import logger

from src.db import db
from src.repositories.document import DocumentRepository, DocumentUpdate
from src.services.rag_pipeline import RagPipeline


async def run_rag_pipeline(
    pipeline: RagPipeline, document_id: int, file_data: dict
) -> None:
    filename = file_data["filename"]
    content = file_data["content"]

    async with db.session() as session:
        repo = DocumentRepository(session)

        await repo.update(document_id, DocumentUpdate(status="processing"))

        try:
            await pipeline.run(document_id, content, filename)
            await repo.update(document_id, DocumentUpdate(status="completed"))

            logger.bind(document_id=document_id, filename=filename).info("Pipeline RAG concluído com sucesso")

        except Exception as e:
            logger.bind(document_id=document_id, filename=filename).exception("Pipeline RAG falhou")

            await repo.update(
                document_id,
                DocumentUpdate(
                    status="failed",
                    error_detail=str(e),
                )
            )
