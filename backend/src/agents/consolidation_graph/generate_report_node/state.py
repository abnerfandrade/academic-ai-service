from langchain.agents import AgentState


class GenerateReportState(AgentState):
    session_id: int
    document_id: int
    class_name: str
