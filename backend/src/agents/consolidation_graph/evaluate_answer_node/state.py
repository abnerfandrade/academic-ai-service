from langchain.agents import AgentState


class EvaluateAnswerState(AgentState):
    session_id: int
    document_id: int
    class_name: str
