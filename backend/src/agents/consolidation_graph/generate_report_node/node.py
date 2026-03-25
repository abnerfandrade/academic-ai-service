from collections import defaultdict
from typing import Dict, Any, List
from datetime import datetime, timezone

from loguru import logger
from langchain_core.messages import AIMessage, HumanMessage

from src.agents.consolidation_graph.state import ConsolidationState
from src.db.database import db
from src.repositories.session_report.repository import SessionReportRepository
from src.repositories.session_report.datatypes import SessionReportCreate
from src.repositories.session.repository import SessionRepository
from src.repositories.session.datatypes import SessionUpdate

from .agent import get_generate_report_agent


async def generate_report(state: ConsolidationState) -> Dict[str, Any]:
    """
    Node do LangGraph responsável por gerar o relatório final de consolidação,
    avaliando os objetivos dominados e a revisar, e persistindo o resultado.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name", "")
    learning_objectives = state.get("learning_objectives", [])
    answers = state.get("answers", [])

    log = logger.bind(
        graph="consolidation_graph",
        node="generate_report",
        session_id=session_id,
        document_id=document_id
    )
    log.info("Iniciando geração de relatório de consolidação")

    if not answers:
        log.warning("Nenhuma resposta encontrada no estado para gerar relatório.")
        return {}

    metrics = _calculate_metrics(answers, learning_objectives)
    strengths = metrics["strengths"]
    weaknesses = metrics["weaknesses"]
    overall_score = metrics["overall_score"]
    
    log.info(f"Pontuação geral: {overall_score}. Dominados: {len(strengths)}, A Revisar: {len(weaknesses)}")

    mastered_objectives_str = "\n".join([f"- {obj}" for obj in strengths]) if strengths else "Nenhum objetivo dominado."

    to_review_parts = []
    for w in weaknesses:
        justifications = [ans.get("justification", "") for ans in answers if ans.get("concept_tag") == w and not ans.get("is_correct")]
        justification_text = " ".join(justifications) if justifications else "Compreensão incompleta."
        to_review_parts.append(f"- **{w}**\n  Justificativa: {justification_text}")

    to_review_objectives_str = "\n".join(to_review_parts) if to_review_parts else "Nenhum objetivo a revisar. Excelente!"

    agent = get_generate_report_agent(
        class_name=class_name,
        overall_score=overall_score,
        mastered_objectives_str=mastered_objectives_str,
        to_review_objectives_str=to_review_objectives_str
    )

    input_data = {
        "messages": [HumanMessage(content="Gere o relatório de consolidação de conhecimento.")],
        "session_id": session_id,
        "document_id": document_id,
        "class_name": class_name
    }
    result = await agent.ainvoke(input_data)
    
    recommendations_markdown = result['structured_response'].recommendations

    report_data = {
        "overall_score": overall_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations_markdown,
    }

    await _persist_report_and_complete_session(session_id, report_data, answers, log)

    closing_message = "Seu relatório de consolidação está pronto. Você já pode visualizar o seu diagnóstico pedagógico!"

    return {
        "report": {**report_data, "questions": answers},
        "messages": [AIMessage(content=closing_message)]
    }


def _calculate_metrics(answers: List[Dict[str, Any]], learning_objectives: List[str]) -> Dict[str, Any]:
    """Calcula a pontuação geral baseada nos objetivos dominados vs total de objetivos avaliados."""
    concept_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    for ans in answers:
        tag = ans.get("concept_tag")
        if not tag:
            continue

        concept_stats[tag]["total"] += 1
        if ans.get("is_correct"):
            concept_stats[tag]["correct"] += 1

    strengths = []
    weaknesses = []

    tested_objectives = list(concept_stats.keys())
    for tag in tested_objectives:
        stats = concept_stats[tag]
        accuracy = stats["correct"] / stats["total"]
        if accuracy > 0.5:
            strengths.append(tag)
        else:
            weaknesses.append(tag)

    total_objectives = len(tested_objectives)
    overall_score = len(strengths) / total_objectives if total_objectives > 0 else 0.0

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
                    case_type="case2",
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

        log.info("Relatório de consolidação salvo e sessão marcada como 'completed'.")
    except Exception as e:
        log.error(f"Erro ao persistir o relatório de consolidação: {e}")
        raise
