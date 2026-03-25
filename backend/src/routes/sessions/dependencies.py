from fastapi import Request
from langchain_core.runnables import Runnable

from src.agents.leveling_graph.graph import build_leveling_graph
from src.agents.consolidation_graph.graph import build_consolidation_graph


def get_graph(case_type: str, request: Request) -> Runnable:
    """
    Retorna o grafo correto com base no case_type.
    """
    checkpointer = request.app.state.checkpointer

    if case_type == "case2":
        return build_consolidation_graph(checkpointer)

    return build_leveling_graph(checkpointer)
