from loguru import logger
from langchain_core.messages import AIMessage

from src.agents.consolidation_graph.state import ConsolidationState
from src.db.database import db
from src.repositories.session_message import SessionMessageRepository, SessionMessageCreate


async def acknowledge_answers(state: ConsolidationState):
    """
    Node que apenas retorna uma mensagem de agradecimento informando
    que o diagnóstico está sendo gerado.
    """
    session_id = state.get("session_id")
    log = logger.bind(
        graph="consolidation_graph",
        node="acknowledge_answers",
        session_id=session_id
    )
    log.info("Agradecendo pelas respostas. O diagnóstico será gerado.")

    content = "Obrigado por responder a todas as perguntas! Estamos gerando o seu diagnóstico..."
    message = AIMessage(content=content)

    await _persist_session_message(session_id, content, log)

    return {"messages": [message]}


async def _persist_session_message(session_id: int, content: str, log) -> None:
    if not session_id:
        return

    try:
        async with db.session() as session:
            repo = SessionMessageRepository(session)
            await repo.create(
                SessionMessageCreate(
                    session_id=session_id,
                    type="ai",
                    content=content,
                )
            )
        log.info("Mensagem de acknowledge persistida em session_messages")
    except Exception as e:
        log.error(f"Erro ao persistir mensagem de acknowledge: {e}")
        raise
