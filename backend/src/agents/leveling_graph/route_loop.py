from src.agents.leveling_graph.state import LevelingState
from src.core.logger import logger


def route_loop(state: LevelingState) -> str:
    """
    Função condicional (edge) do LangGraph que decide o próximo passo:
    continuar perguntando ('ask_question') ou finalizar ('generate_report').
    """
    questions = state.get("questions", [])
    current_index = state.get("current_index", 0)
    session_id = state.get("session_id")

    log = logger.bind(
        graph="leveling_graph",
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
