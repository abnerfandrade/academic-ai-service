import asyncio
from loguru import logger

from src.services.rag_pipeline.extractor import DocumentExtractor
from src.services.rag_pipeline.chunker import TokenChunker
from src.services.rag_pipeline.embedder import Embedder
from src.services.rag_pipeline.objective_extractor import ObjectiveExtractor


class RagPipeline:
    def __init__(self):
        self.logger = logger.bind(service="rag_pipeline")
        self._extractor = DocumentExtractor()
        self._chunker = TokenChunker()
        self._embedder = Embedder()
        self._objective_extractor = ObjectiveExtractor()

    async def run(
        self,
        document_id: int,
        content: bytes,
        filename: str,
    ) -> dict:
        self.logger = self.logger.bind(filename=filename)

        text = await self.step_1(content, filename)
        chunks = await self.step_2(text, filename, document_id)
        stored = await self.step_3(chunks, filename)
        objectives = await self.step_4(text, document_id)

        return {
            "filename": filename,
            "char_count": len(text),
            "chunk_count": len(chunks),
            "stored_count": stored,
            "prerequisites": objectives["prerequisites"],
            "learning_objectives": objectives["learning_objectives"],
        }

    async def step_1(self, content: bytes, filename: str) -> str:
        self.logger.info(f"[EXTRACTING] Iniciando extração de '{filename}'")

        try:
            text = await self._extractor.extract(content, filename)
            self.logger.info(f"[EXTRACTING] {len(text)} chars extraídos")

            return text
        except Exception as e:
            self.logger.exception(f"Falha na extração de '{filename}' | erro={e}")
            raise RuntimeError(f"Falha na extração do documento '{filename}': {e}") from e

    async def step_2(self, text: str, filename: str, document_id: int) -> list[dict]:
        self.logger.info(f"[CHUNKING] Dividindo '{filename}' em chunks")

        try:
            chunks = await asyncio.to_thread(
                self._chunker.chunk, text, filename=filename, document_id=document_id
            )
            self.logger.info(f"[CHUNKING] {len(chunks)} chunks criados")

            return chunks
        except Exception as e:
            self.logger.exception(f"Falha no chunking de '{filename}' | erro={e}")
            raise RuntimeError(f"Falha ao dividir o documento '{filename}' em chunks: {e}") from e

    async def step_3(self, chunks: list[dict], filename: str) -> int:
        self.logger.info(f"[EMBEDDING] Gerando embeddings e salvando {len(chunks)} chunks de '{filename}' no Qdrant")

        try:
            stored = await asyncio.to_thread(self._embedder.embed_and_store, chunks)
            self.logger.info(f"[EMBEDDING] {stored} chunks de '{filename}' salvos com sucesso")

            return stored
        except Exception as e:
            self.logger.exception(f"Falha no embedding/armazenamento de '{filename}' | erro={e}")
            raise RuntimeError(
                f"Falha ao gerar embeddings ou armazenar chunks de '{filename}': {e}"
            ) from e

    async def step_4(self, text: str, document_id: int) -> dict:
        self.logger.info(f"[OBJECTIVES] Extraindo pré-requisitos e objetivos de aprendizado do documento '{document_id}'")
        try:
            objectives = await self._objective_extractor.extract(text, document_id)
            self.logger.info(f"[OBJECTIVES] Pré-requisitos e objetivos de aprendizado extraídos com sucesso")

            return objectives
        except Exception as e:
            self.logger.exception(f"Falha na extração de objetivos do documento '{document_id}' | erro={e}")
            raise RuntimeError(f"Falha na extração de objetivos do documento '{document_id}': {e}") from e
