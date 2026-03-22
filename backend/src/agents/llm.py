
from functools import lru_cache
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from src.core.config import settings
from src.core.logger import logger


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    if settings.LLM_PROVIDER == "gemini":
        logger.debug(f"LLM provider: gemini | model: {settings.GEMINI_MODEL}")
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY
        )
    elif settings.LLM_PROVIDER == "openai":
        logger.debug(f"LLM provider: openai | model: {settings.OPENAI_MODEL}")
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY
        )

    raise ValueError(f"Provedor de LLM não suportado: {settings.LLM_PROVIDER}")
