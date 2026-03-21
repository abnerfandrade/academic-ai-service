from loguru import logger
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from src.services.vector_store.store import get_vector_store


class VectorStoreRetriever:
    def __init__(self, k: int = 5, vector_store: QdrantVectorStore | None = None):
        self.logger = logger.bind(service="vector_store_retriever", k=k)
        self.vector_store = vector_store or get_vector_store(for_query=True)
        self._k = k

    def search(self, query: str) -> list[Document]:
        self.logger.debug(f"Buscando documentos similares | query='{query[:80]}...'")

        try:
            results = self.vector_store.similarity_search(query, k=self._k)
            self.logger.info(f"{len(results)} documentos recuperados")
            return results

        except Exception as e:
            self.logger.exception(f"Falha na busca por similaridade | erro={str(e)}")
            raise
