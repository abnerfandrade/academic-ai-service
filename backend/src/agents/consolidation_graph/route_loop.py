from loguru import logger

from src.agents.consolidation_graph.state import ConsolidationState


def route_loop(state: ConsolidationState) -> str:
    """
    Função condicional (edge) do LangGraph que decide o próximo passo:
    continuar perguntando ('ask_question') ou finalizar ('generate_report').
    """
    questions = state.get("questions", [])
    current_index = state.get("current_index", 0)
    session_id = state.get("session_id")

    log = logger.bind(
        graph="consolidation_graph",
        node="route_loop",
        session_id=session_id,
        current_index=current_index,
        total_questions=len(questions)
    )

    if current_index < len(questions):
        log.info("Ainda há perguntas. Roteando para 'ask_question'.")
        return "ask_question"
    else:
        log.info("Todas as perguntas foram respondidas. Roteando para 'acknowledge_answers'.")
        return "acknowledge_answers"
