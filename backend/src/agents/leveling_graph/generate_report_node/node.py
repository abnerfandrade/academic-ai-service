from typing import Dict, Any, List
from datetime import datetime, timezone

from langchain_core.messages import AIMessage, HumanMessage

from src.core.logger import logger
from src.agents.leveling_graph.state import LevelingState
from src.db.database import db
from src.repositories.session_report.repository import SessionReportRepository
from src.repositories.session_report.datatypes import SessionReportCreate
from src.repositories.session.repository import SessionRepository
from src.repositories.session.datatypes import SessionUpdate

from .agent import get_generate_report_agent


async def generate_report(state: LevelingState) -> Dict[str, Any]:
    """
    Node do LangGraph responsável por gerar o relatório final de nivelamento,
    avaliando os pontos fortes e fracos do aluno e persistindo o resultado.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name", "")
    answers = state.get("answers", [])

    log = logger.bind(
        graph="leveling_graph",
        node="generate_report",
        session_id=session_id,
        document_id=document_id
    )
    log.info("Iniciando geração de relatório")

    if not answers:
        log.warning("Nenhuma resposta encontrada no estado para gerar relatório.")
        return {}

    metrics = _calculate_metrics(answers)
    strengths = metrics["strengths"]
    weaknesses = metrics["weaknesses"]
    log.info(f"Pontuação geral: {metrics['overall_score']}. Fortalezas: {len(strengths)}, Fraquezas: {len(weaknesses)}")

    weaknesses_str = ", ".join(weaknesses) if weaknesses else "Nenhuma fraqueza identificada. O aluno dominou todos os pré-requisitos testados!"
    strengths_str = ", ".join(strengths) if strengths else "Nenhuma fortaleza claramente identificada neste questionário."

    agent = get_generate_report_agent(class_name, weaknesses_str, strengths_str)

    input_data = {
        "messages": [HumanMessage(content="Gere as recomendações e o relatório de nivelamento considerando os pontos fortes e fracos do aluno.")],
        "session_id": session_id,
        "document_id": document_id,
        "class_name": class_name
    }
    result = await agent.ainvoke(input_data)
    
    recommendations_markdown = result['structured_response'].recommendations

    report_data = {
        **metrics,
        "recommendations": recommendations_markdown,
        "questions": answers
    }

    await _persist_report_and_complete_session(session_id, report_data, answers, log)

    closing_message = "Seu relatório de nivelamento está pronto. Você já pode visualizar o seu resultado!"

    return {
        "report": report_data,
        "messages": [AIMessage(content=closing_message)]
    }


def _calculate_metrics(answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula a pontuação geral e separa as tags de conceitos em fortalezas e fraquezas."""
    total_questions = len(answers)
    correct_answers = [ans for ans in answers if ans.get("is_correct")]

    overall_score = len(correct_answers) / total_questions if total_questions > 0 else 0.0
    strengths = [ans.get("concept_tag") for ans in answers if ans.get("is_correct")]
    weaknesses = [ans.get("concept_tag") for ans in answers if not ans.get("is_correct")]

    return {
        "overall_score": overall_score,
        "strengths": strengths,
        "weaknesses": weaknesses
    }


async def _persist_report_and_complete_session(
    session_id: int,
    report_data: Dict[str, Any],
    answers: List[Dict[str, Any]],
    log: Any
) -> None:
    """Salva o relatório no banco de dados e marca a sessão como 'completed'."""
    if not session_id:
        return

    try:
        async with db.session() as session:
            report_repo = SessionReportRepository(session)
            await report_repo.create(
                SessionReportCreate(
                    session_id=session_id,
                    case_type="case1",
                    questions=answers,
                    overall_score=report_data["overall_score"],
                    strengths=report_data["strengths"],
                    weaknesses=report_data["weaknesses"],
                    recommendations=report_data["recommendations"]
                )
            )

            session_repo = SessionRepository(session)
            await session_repo.update(
                session_id,
                SessionUpdate(
                    status="completed",
                    completed_at=datetime.now(timezone.utc)
                )
            )

        log.info("Relatório salvo e sessão marcada como 'completed'.")
    except Exception as e:
        log.error(f"Erro ao persistir o relatório: {e}")
        raise
