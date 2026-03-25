from langchain_core.messages import HumanMessage
from loguru import logger

from src.agents.consolidation_graph.state import ConsolidationState
from .agent import get_generate_questions_agent


async def generate_questions(state: ConsolidationState):
    """
    Node do LangGraph responsável por gerar uma lista de perguntas
    baseadas nos objetivos de aprendizado da aula.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name")
    learning_objectives = state.get("learning_objectives", [])

    log = logger.bind(
        graph="consolidation_graph",
        node="generate_questions",
        session_id=session_id,
        document_id=document_id,
        class_name=class_name,
    )
    log.info(f"Iniciando geração de perguntas")

    agent = get_generate_questions_agent()

    learning_objectives_str = "\n".join([f"- {lo}" for lo in learning_objectives])
    message = HumanMessage(content=f"Objetivos de aprendizado:\n{learning_objectives_str}")

    input_data = {
        "messages": [message],
        "session_id": session_id,
        "document_id": document_id,
        "class_name": class_name
    }
    result = await agent.ainvoke(input_data)

    questions_objects = result['structured_response'].questions
    questions = [{"question": q.question, "concept_tag": q.concept_tag} for q in questions_objects]

    log.info(f"Foram geradas {len(questions)} perguntas")

    return {
        "questions": questions,
        "current_index": 0
    }
