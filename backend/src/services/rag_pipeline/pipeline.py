import asyncio

from src.core.logger import logger
from src.services.rag_pipeline.extractor import DocumentExtractor
from src.services.rag_pipeline.chunker import TokenChunker
from src.services.rag_pipeline.embedder import Embedder


class RagPipeline:
    def __init__(self):
        self.logger = logger.bind(service="rag_pipeline")
        self._extractor = DocumentExtractor()
        self._chunker = TokenChunker()
        self._embedder = Embedder()

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

        return {
            "filename": filename,
            "char_count": len(text),
            "chunk_count": len(chunks),
            "stored_count": stored,
        }

    async def step_1(self, content: bytes, filename: str) -> str:
        self.logger.info(f"[EXTRACTING] Iniciando extração de '{filename}'")

        try:
            text = await self._extractor.extract(content, filename)
            self.logger.info(f"[EXTRACTED] {len(text)} chars extraídos")

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

            self.logger.info(f"[CHUNKED] {len(chunks)} chunks criados")

            return chunks
        except Exception as e:
            self.logger.exception(f"Falha no chunking de '{filename}' | erro={e}")
            raise RuntimeError(f"Falha ao dividir o documento '{filename}' em chunks: {e}") from e

    async def step_3(self, chunks: list[dict], filename: str) -> int:
        self.logger.info(f"[EMBEDDING] Gerando embeddings e salvando {len(chunks)} chunks de '{filename}' no Qdrant")

        try:
            stored = await asyncio.to_thread(self._embedder.embed_and_store, chunks)
            self.logger.info(f"[DONE] {stored} chunks de '{filename}' salvos com sucesso")

            return stored
        except Exception as e:
            self.logger.exception(f"Falha no embedding/armazenamento de '{filename}' | erro={e}")
            raise RuntimeError(
                f"Falha ao gerar embeddings ou armazenar chunks de '{filename}': {e}"
            ) from e
