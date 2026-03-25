from functools import lru_cache
from langchain.agents import create_agent

from src.agents.llm import get_llm
from .state import GenerateQuestionsState
from .prompt import SYSTEM_PROMPT
from .tools import search_chunks_for_learning_objectives
from .datatypes import QuestionsOutput
from src.core.config import settings


@lru_cache(maxsize=1)
def get_generate_questions_agent():
    formatted_prompt = SYSTEM_PROMPT.format(
        num_questions=settings.CONSOLIDATION_NUM_QUESTIONS
    )

    return create_agent(
        model=get_llm(),
        tools=[search_chunks_for_learning_objectives],
        name="generate_questions_agent",
        system_prompt=formatted_prompt,
        response_format=QuestionsOutput,
        state_schema=GenerateQuestionsState,
    )
