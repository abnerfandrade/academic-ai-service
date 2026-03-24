from loguru import logger

from src.db import db
from src.repositories.document import DocumentRepository, DocumentUpdate
from src.services.rag_pipeline import RagPipeline


async def run_rag_pipeline(
    pipeline: RagPipeline, document_id: int, file_data: dict
) -> None:
    filename = file_data["filename"]
    content = file_data["content"]
    log = logger.bind(document_id=document_id, filename=filename)
    log.info("Iniciando pipeline RAG")

    async with db.session() as session:
        repo = DocumentRepository(session)

        await repo.update(document_id, DocumentUpdate(status="processing"), commit=True)

        try:
            result = await pipeline.run(document_id, content, filename)

            data_upd = DocumentUpdate(
                prerequisites=result["prerequisites"],
                learning_objectives=result["learning_objectives"],
                status="completed",
            )
            await repo.update(document_id, data_upd)

            log.info("Pipeline RAG concluído com sucesso")

        except Exception as e:
            log.exception("Pipeline RAG falhou")

            await repo.update(
                document_id,
                DocumentUpdate(
                    status="failed",
                    error_detail=str(e),
                )
            )
