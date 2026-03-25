import asyncio
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage
from loguru import logger

from src.agents.consolidation_graph.state import ConsolidationState
from src.db.database import db
from src.repositories.session_message import SessionMessageRepository, SessionMessageCreate
from .agent import get_evaluate_answer_agent


async def evaluate_answer(state: ConsolidationState) -> Dict[str, Any]:
    """
    Node do LangGraph responsável por avaliar a resposta de consolidação do aluno,
    persistir o histórico e atualizar o estado da sessão.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name")
    questions = state.get("questions", [])
    current_index = state.get("current_index", 0)
    messages = state.get("messages", [])
    answers = state.get("answers", [])

    log = logger.bind(
        graph="consolidation_graph",
        node="evaluate_answer",
        session_id=session_id,
        document_id=document_id,
        class_name=state.get("class_name"),
        current_index=current_index,
    )
    log.info("Iniciando avaliação da resposta de consolidação")

    if not _is_valid_state(messages, questions, current_index):
        log.warning("Estado inválido: sem mensagens ou current_index fora dos limites.")
        return {}

    student_answer = messages[-1].content
    current_question = questions[current_index]

    await _persist_student_message(session_id, student_answer, log)

    question_text = current_question.get("question", "")
    objective = current_question.get("concept_tag", "")

    agent = get_evaluate_answer_agent(objective=objective, question=question_text)

    input_data = {
        "messages": [HumanMessage(content=f"Resposta do aluno: {student_answer}")],
        "session_id": session_id,
        "document_id": document_id,
        "class_name": class_name,
    }
    result = await agent.ainvoke(input_data)

    evaluation = result['structured_response']
    
    log.info(f"Avaliação concluída. is_correct={evaluation.is_correct}, justification={evaluation.justification}")

    answer_obj = {
        "question": current_question.get("question", ""),
        "student_answer": student_answer,
        "is_correct": evaluation.is_correct,
        "concept_tag": current_question.get("concept_tag", ""),
        "justification": evaluation.justification
    }

    new_answers = list(answers) + [answer_obj]
    new_current_index = current_index + 1

    return {
        "answers": new_answers,
        "current_index": new_current_index
    }


def _is_valid_state(messages: List, questions: List, current_index: int) -> bool:
    """Verifica se o estado possui os dados mínimos necessários para a avaliação."""
    return bool(messages and questions and current_index < len(questions))


async def _persist_student_message(session_id: int, student_answer: str, log: Any) -> None:
    """Salva a mensagem do aluno no banco de dados para histórico."""
    if not session_id:
        return

    try:
        async with db.session() as session:
            repo = SessionMessageRepository(session)
            await repo.create(
                SessionMessageCreate(
                    session_id=session_id,
                    type="human",
                    content=student_answer,
                )
            )

        log.info("Mensagem do aluno persistida em session_messages")
    except Exception as e:
        log.error(f"Erro ao persistir mensagem do aluno: {e}")
        raise


async def _evaluate_student_answer(state: ConsolidationState, current_question: Dict[str, Any], student_answer: str) -> Any:
    """Invoca o agente de avaliação para analisar a resposta do aluno."""
    question_text = current_question.get("question", "")
    objective = current_question.get("concept_tag", "")

    agent = get_evaluate_answer_agent(objective=objective, question=question_text)
    input_data = {
        **state,
        "messages": [HumanMessage(content=f"Resposta do aluno: {student_answer}")]
    }

    result = await agent.ainvoke(input_data)
    return result['structured_response']
