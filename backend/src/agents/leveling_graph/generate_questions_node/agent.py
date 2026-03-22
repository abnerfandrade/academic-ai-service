from functools import lru_cache
from langchain.agents import create_agent, AgentState

from src.agents.llm import get_llm
from .prompt import SYSTEM_PROMPT
from .datatypes import QuestionsOutput
from src.core.config import settings


@lru_cache(maxsize=50)
def get_generate_questions_agent(prerequisites: str):
    formatted_prompt = SYSTEM_PROMPT.format(
        prerequisites=prerequisites,
        num_questions=settings.LEVELING_NUM_QUESTIONS
    )

    return create_agent(
        model=get_llm(),
        tools=[],
        name="generate_questions_agent",
        system_prompt=formatted_prompt,
        response_format=QuestionsOutput,
    )
