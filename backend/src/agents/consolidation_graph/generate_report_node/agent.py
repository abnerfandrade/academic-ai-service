from functools import lru_cache
from langchain.agents import create_agent

from src.agents.llm import get_llm
from .prompt import SYSTEM_PROMPT
from .tools import search_chunks_for_revision
from .state import GenerateReportState
from .datatypes import GenerateReportOutput


def get_generate_report_agent(class_name: str, overall_score: float, mastered_objectives_str: str, to_review_objectives_str: str):
    formatted_prompt = SYSTEM_PROMPT.format(
        class_name=class_name,
        overall_score=f"{overall_score:.2f}",
        mastered_objectives_str=mastered_objectives_str,
        to_review_objectives_str=to_review_objectives_str
    )

    return create_agent(
        model=get_llm(),
        tools=[search_chunks_for_revision],
        name="generate_report_agent",
        system_prompt=formatted_prompt,
        response_format=GenerateReportOutput,
        state_schema=GenerateReportState,
    )
