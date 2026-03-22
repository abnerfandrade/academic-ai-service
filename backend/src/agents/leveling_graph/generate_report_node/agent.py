from functools import lru_cache
from langchain.agents import create_agent

from src.agents.llm import get_llm
from .prompt import SYSTEM_PROMPT
from .tools import search_document_chunks_for_concepts
from .state import GenerateReportState
from .datatypes import GenerateReportOutput


@lru_cache(maxsize=50)
def get_generate_report_agent(class_name: str, weaknesses_str: str, strengths_str: str):
    formatted_prompt = SYSTEM_PROMPT.format(
        class_name=class_name,
        weaknesses_str=weaknesses_str,
        strengths_str=strengths_str
    )

    return create_agent(
        model=get_llm(),
        tools=[search_document_chunks_for_concepts],
        name="generate_report_agent",
        system_prompt=formatted_prompt,
        response_format=GenerateReportOutput,
        state_schema=GenerateReportState,
    )
