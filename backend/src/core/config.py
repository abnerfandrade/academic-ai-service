import os
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    ENVIRONMENT: Literal["development", "production"] = Field(default="development", description="Ambiente de execução")
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO", description="Nível de log")
    DATABASE_URL: str = Field(..., description="URL de conexão com o banco de dados (postgresql+psycopg://)")
    CHECKPOINTER_URL: str = Field(..., description="URL de conexão para o checkpointer LangGraph (postgresql://)")
    LLM_PROVIDER: Literal["gemini", "openai"] = Field(default="gemini", description="Provedor de LLM a ser utilizado")
    GEMINI_API_KEY: str = Field(..., description="Chave de API do Gemini")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="Modelo do Gemini a ser utilizado")
    GEMINI_EMBEDDING_MODEL: str = Field(default="gemini-embedding-001", description="Modelo de embedding do Gemini a ser utilizado")
    OPENAI_API_KEY: str = Field(..., description="Chave de API da OpenAI")
    OPENAI_MODEL: str = Field(default="gpt-5-mini", description="Modelo da OpenAI a ser utilizado")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", description="Modelo de embedding da OpenAI a ser utilizado")
    QDRANT_URL: str = Field(..., description="URL do Qdrant")
    QDRANT_COLLECTION_NAME: str = Field(..., description="Nome da coleção no Qdrant")
    QDRANT_VECTOR_SIZE: int = Field(..., description="Tamanho da dimensão do vetor no Qdrant")
    CHUNK_SIZE_TOKENS: int = Field(default=1024, description="Tamanho do chunk em tokens")
    CHUNK_OVERLAP_TOKENS: int = Field(default=154, description="Sobreposição do chunk em tokens")
    MAX_UPLOAD_SIZE_MB: int = Field(default=10, description="Tamanho máximo de upload em MB")
    LEVELING_NUM_QUESTIONS: int = Field(default=5, description="Número de questões na etapa de nivelamento")
    CONSOLIDATION_NUM_QUESTIONS: int = Field(default=10, description="Número de questões na etapa de consolidação")

    LANGSMITH_TRACING: bool = Field(default=False, description="Habilitar tracing no LangSmith")
    LANGSMITH_API_KEY: str = Field("", description="Chave de API do LangSmith")
    LANGSMITH_PROJECT: str = Field("", description="Projeto no LangSmith")
    LANGSMITH_ENDPOINT: str = Field("", description="Endpoint do LangSmith")

    def configure_langsmith(self) -> None:
        """Configura as variáveis de ambiente para LangSmith."""
        os.environ["LANGSMITH_TRACING"] = str(self.LANGSMITH_TRACING).lower()
        os.environ["LANGSMITH_API_KEY"] = self.LANGSMITH_API_KEY
        os.environ["LANGSMITH_PROJECT"] = self.LANGSMITH_PROJECT
        os.environ["LANGSMITH_ENDPOINT"] = self.LANGSMITH_ENDPOINT


settings = Settings()
