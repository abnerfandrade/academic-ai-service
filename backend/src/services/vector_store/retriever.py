from loguru import logger
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import models

from src.services.vector_store.store import get_vector_store


class VectorStoreRetriever:
    def __init__(self, vector_store: QdrantVectorStore | None = None):
        self.logger = logger.bind(service="vector_store_retriever")
        self.vector_store = vector_store or get_vector_store(for_query=True)

    def search(self, query: str, k: int = 5, score_threshold: float = 0.75, filter: models.Filter | None = None) -> list[Document]:
        self.logger.debug(f"Buscando documentos similares | query='{query[:80]}...'")

        try:
            results = self.vector_store.similarity_search(
                query, k=k, filter=filter, score_threshold=score_threshold
            )
            self.logger.info(f"{len(results)} documentos recuperados")
            return results

        except Exception as e:
            self.logger.exception(f"Falha na busca por similaridade | erro={str(e)}")
            raise
