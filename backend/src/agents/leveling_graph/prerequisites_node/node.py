from langchain_core.messages import HumanMessage

from src.core.logger import logger
from src.agents.leveling_graph.state import LevelingState
from .agent import get_prerequisites_agent


async def extract_prerequisites(state: LevelingState):
    """
    Node do LangGraph responsável por extrair os pré-requisitos de uma aula usando um agente LLM.
    """
    session_id = state.get("session_id")
    document_id = state.get("document_id")
    class_name = state.get("class_name")

    log = logger.bind(
        graph="leveling_graph",
        node="extract_prerequisites",
        session_id=session_id,
        document_id=document_id,
        class_name=class_name,
    )
    log.info(f"Iniciando extração de pré-requisitos")

    agent = get_prerequisites_agent(class_name)

    input = {
        "messages": [HumanMessage(content="Analise a aula e extraia os pré-requisitos.")],
        "session_id": session_id,
        "document_id": document_id,
        "class_name": class_name
    }
    result = await agent.ainvoke(input, config={"recursion_limit": 6})

    prerequisites = result['structured_response'].concept_tags

    log.info(f"Pré-requisitos extraídos: {prerequisites}")

    return {"prerequisites": prerequisites}
