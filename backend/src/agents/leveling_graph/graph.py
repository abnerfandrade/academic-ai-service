from typing import Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from .state import LevelingState
from .generate_questions_node.node import generate_questions
from .ask_question_node.node import ask_question
from .evaluate_answer_node.node import evaluate_answer
from .route_loop import route_loop
from .acknowledge_answers_node.node import acknowledge_answers
from .generate_report_node.node import generate_report


def build_leveling_graph(checkpointer: Optional[AsyncPostgresSaver] = None):
    builder = StateGraph(LevelingState)

    builder.add_node("generate_questions", generate_questions)
    builder.add_node("ask_question", ask_question)
    builder.add_node("evaluate_answer", evaluate_answer)
    builder.add_node("acknowledge_answers", acknowledge_answers)
    builder.add_node("generate_report", generate_report)

    builder.add_edge(START, "generate_questions")
    builder.add_edge("generate_questions", "ask_question")
    builder.add_edge("ask_question", "evaluate_answer")

    builder.add_conditional_edges(
        "evaluate_answer",
        route_loop,
        {
            "ask_question": "ask_question",
            "acknowledge_answers": "acknowledge_answers"
        }
    )

    builder.add_edge("acknowledge_answers", "generate_report")
    builder.add_edge("generate_report", END)

    return builder.compile(
        checkpointer=checkpointer,
        interrupt_after=["ask_question", "acknowledge_answers"],
    )
