import uuid

from loguru import logger
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.exceptions import UnexpectedResponse

from src.services.vector_store.store import get_vector_store


class Embedder:
    def __init__(self, vector_store: QdrantVectorStore | None = None):
        self.logger = logger.bind(service="embedder")
        self.vector_store = vector_store or get_vector_store()

    def embed_and_store(self, chunks: list[dict]) -> int:
        if not chunks:
            self.logger.warning("Nenhum chunk recebido para armazenar")
            return 0

        try:
            documents = [
                Document(page_content=c["content"], metadata=c["metadata"])
                for c in chunks
            ]
            ids = [
                str(uuid.uuid5(uuid.NAMESPACE_DNS, c["metadata"]["chunk_id"]))
                for c in chunks
            ]

            self.logger.debug(f"Gerando embeddings e armazenando {len(documents)} chunks no Qdrant")
            self.vector_store.add_documents(documents=documents, ids=ids)

            self.logger.info(f"{len(documents)} chunks armazenados com sucesso")
            return len(documents)

        except UnexpectedResponse as e:
            self.logger.exception(f"Resposta inesperada do Qdrant ao armazenar chunks | status={e.status_code}")
            raise
        except Exception as e:
            self.logger.exception(f"Falha ao gerar embeddings ou armazenar chunks no Qdrant | erro={e}")
            raise
