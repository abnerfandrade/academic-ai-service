from functools import lru_cache
from langchain.agents import create_agent, AgentState

from src.agents.llm import get_llm
from .prompt import SYSTEM_PROMPT
from .datatypes import EvaluationOutput


@lru_cache(maxsize=50)
def get_evaluate_answer_agent(concept_tag: str, question: str):
    formatted_prompt = SYSTEM_PROMPT.format(
        concept_tag=concept_tag,
        question=question
    )

    return create_agent(
        model=get_llm(),
        tools=[],
        name="evaluate_answer_agent",
        system_prompt=formatted_prompt,
        response_format=EvaluationOutput,
    )
