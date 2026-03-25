from langchain.agents import create_agent

from src.agents.llm import get_llm
from .state import EvaluateAnswerState
from .prompt import SYSTEM_PROMPT
from .datatypes import EvaluationOutput
from .tools import search_chunks_for_evaluation


def get_evaluate_answer_agent(objective: str, question: str):
    formatted_prompt = SYSTEM_PROMPT.format(
        objective=objective,
        question=question
    )

    return create_agent(
        model=get_llm(),
        tools=[search_chunks_for_evaluation],
        name="evaluate_answer_agent",
        system_prompt=formatted_prompt,
        response_format=EvaluationOutput,
        state_schema=EvaluateAnswerState,
    )
