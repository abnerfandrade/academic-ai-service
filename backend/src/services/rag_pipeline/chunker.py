import tiktoken
from loguru import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.config import settings

_encoding = tiktoken.get_encoding("cl100k_base")


def _tiktoken_len(text: str) -> int:
    return len(_encoding.encode(text))


class TokenChunker:
    def __init__(self):
        self.logger = logger.bind(service="chunker")
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE_TOKENS,
            chunk_overlap=settings.CHUNK_OVERLAP_TOKENS,
            length_function=_tiktoken_len,
            separators=["\n\n", "\n", " ", ""],
        )

    def chunk(self, text: str, filename: str, document_id: int) -> list[dict]:
        if not text or not text.strip():
            raise ValueError(f"Texto vazio ou sem conteúdo para dividir em chunks (filename='{filename}')")

        try:
            raw_chunks = self._splitter.split_text(text)
            if not raw_chunks:
                raise ValueError(f"Nenhum chunk gerado para '{filename}' (texto com {len(text)} chars)")

            total_chunks = len(raw_chunks)
            chunks = [
                {
                    "content": chunk,
                    "metadata": {
                        "chunk_id": f"{document_id}::chunk::{i}",
                        "chunk_index": i,
                        "total_chunks": total_chunks,
                        "document_id": document_id,
                        "filename": filename,
                    },
                }
                for i, chunk in enumerate(raw_chunks)
            ]

            self.logger.info(
                f"{len(chunks)} chunks criados | "
                f"tamanho={settings.CHUNK_SIZE_TOKENS} tokens, "
                f"overlap={settings.CHUNK_OVERLAP_TOKENS} tokens"
            )
            return chunks

        except Exception as e:
            self.logger.exception(f"Erro ao dividir texto de '{filename}' em chunks | erro={e}")
            raise
