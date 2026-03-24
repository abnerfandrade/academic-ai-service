from langchain_core.messages import HumanMessage

from src.core.logger import logger
from src.agents.leveling_graph.state import LevelingState
from .agent import get_generate_questions_agent


async def generate_questions(state: LevelingState):
    """
    Node do LangGraph responsável por gerar uma lista de perguntas
    baseadas nos pré-requisitos extraídos no passo anterior.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name")
    prerequisites = state.get("prerequisites", [])

    log = logger.bind(
        graph="leveling_graph",
        node="generate_questions",
        session_id=session_id,
        document_id=document_id,
        class_name=class_name,
    )
    log.info(f"Iniciando geração de perguntas")

    prereqs_str = "\n".join([f"- {p}" for p in prerequisites])
    agent = get_generate_questions_agent(prereqs_str)

    input_data = {
        "messages": [HumanMessage(content="Analise os prerequisitos da aula e gere perguntas.")]
    }
    result = await agent.ainvoke(input_data)

    questions_objects = result['structured_response'].questions
    questions = [{"question": q.question, "concept_tag": q.concept_tag} for q in questions_objects]

    log.info(f"Foram geradas {len(questions)} perguntas")

    return {
        "questions": questions,
        "current_index": 0
    }
