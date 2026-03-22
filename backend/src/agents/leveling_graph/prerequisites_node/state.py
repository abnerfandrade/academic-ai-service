from langchain.agents import AgentState


class PrerequisitesState(AgentState):
    session_id: int
    document_id: int
    class_name: str
