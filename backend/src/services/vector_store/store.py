from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, SparseVectorParams
from loguru import logger

from src.core.config import settings


def get_embeddings_client(for_query: bool = False) -> Embeddings:
    if settings.LLM_PROVIDER == "gemini":
        logger.debug(
            f"Provedor de embeddings: gemini | modelo: {settings.GEMINI_EMBEDDING_MODEL}"
        )
        return GoogleGenerativeAIEmbeddings(
            model=settings.GEMINI_EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            task_type="RETRIEVAL_QUERY" if for_query else "RETRIEVAL_DOCUMENT",
            output_dimensionality=settings.QDRANT_VECTOR_SIZE
        )
    elif settings.LLM_PROVIDER == "openai":
        logger.debug(
            f"Provedor de embeddings: openai | modelo: {settings.OPENAI_EMBEDDING_MODEL}"
        )
        return OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
            dimensions=settings.QDRANT_VECTOR_SIZE
        )

    raise ValueError(f"Provedor de embeddings não suportado: '{settings.LLM_PROVIDER}'")


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    logger.debug(f"Conectando ao Qdrant em '{settings.QDRANT_URL}'")
    try:
        client = QdrantClient(url=settings.QDRANT_URL)
        logger.debug("Conexão com Qdrant estabelecida com sucesso")
        return client
    except Exception as e:
        logger.error(f"Falha ao conectar ao Qdrant em '{settings.QDRANT_URL}' | erro={e}")
        raise


def get_vector_store(for_query: bool = False) -> QdrantVectorStore:
    try:
        client = get_qdrant_client()

        if not client.collection_exists(settings.QDRANT_COLLECTION_NAME):
            client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config={
                    "dense": VectorParams(
                        size=settings.QDRANT_VECTOR_SIZE,
                        distance=Distance.COSINE,
                    )
                },
                sparse_vectors_config={
                    "sparse": SparseVectorParams()
                },
            )
            logger.info(f"Coleção '{settings.QDRANT_COLLECTION_NAME}' criada no Qdrant")
        else:
            logger.debug(f"Coleção '{settings.QDRANT_COLLECTION_NAME}' já existe no Qdrant")

        return QdrantVectorStore(
            client=client,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            embedding=get_embeddings_client(for_query),
            sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="dense",
            sparse_vector_name="sparse",
        )
    except Exception as e:
        logger.error(
            f"Falha ao inicializar o vector store "
            f"(coleção='{settings.QDRANT_COLLECTION_NAME}') | erro={e}"
        )
        raise
