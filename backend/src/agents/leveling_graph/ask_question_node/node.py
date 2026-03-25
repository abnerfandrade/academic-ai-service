from typing import Any

from langchain_core.messages import AIMessage
from loguru import logger

from src.agents.leveling_graph.state import LevelingState
from src.db.database import db
from src.repositories.session_message import SessionMessageRepository, SessionMessageCreate


async def ask_question(state: LevelingState):
    """
    Node do LangGraph responsável por emitir a pergunta atual para o aluno
    e persistir essa mensagem no banco de dados.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name")
    questions = state.get("questions", [])
    current_index = state.get("current_index", 0)

    log = logger.bind(
        graph="leveling_graph",
        node="ask_question",
        session_id=session_id,
        document_id=document_id,
        class_name=class_name,
        current_index=current_index,
    )
    log.info("Iniciando emissão da pergunta atual")

    if not questions or current_index >= len(questions):
        log.warning("Nenhuma pergunta disponível ou current_index fora dos limites.")
        return {}

    current_question = questions[current_index]
    question_text = current_question.get("question", "")

    message = AIMessage(content=question_text)

    await _persist_session_message(session_id, question_text, log)

    return {"messages": [message]}


async def _persist_session_message(session_id: int, question_text: str, log: Any) -> None:
    """Salva a mensagem do aluno no banco de dados para histórico."""
    if not session_id:
        return

    try:
        async with db.session() as session:
            repo = SessionMessageRepository(session)
            await repo.create(
                SessionMessageCreate(
                    session_id=session_id,
                    type="ai",
                    content=question_text,
                )
            )
        log.info("Mensagem persistida em session_messages no PostgreSQL")
    except Exception as e:
        log.error(f"Erro ao persistir mensagem da sessão: {e}")
        raise
