from langchain.agents import AgentState


class GenerateQuestionsState(AgentState):
    session_id: int
    document_id: int
    class_name: str
