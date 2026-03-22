from functools import lru_cache
from langchain.agents import create_agent, AgentState

from src.agents.llm import get_llm
from .state import PrerequisitesState
from .prompt import SYSTEM_PROMPT
from .tools import search_document_chunks, get_all_document_chunks
from .datatypes import PrerequisitesOutput


@lru_cache(maxsize=50)
def get_prerequisites_agent(class_name: str):
    formatted_prompt = SYSTEM_PROMPT.format(class_name=class_name)

    return create_agent(
        model=get_llm(),
        tools=[search_document_chunks, get_all_document_chunks],
        name="prerequisites_agent",
        system_prompt=formatted_prompt,
        response_format=PrerequisitesOutput,
        state_schema=PrerequisitesState,
    )
