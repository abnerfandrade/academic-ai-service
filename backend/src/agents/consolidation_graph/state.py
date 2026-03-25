from typing import Annotated, Any, Optional
from typing_extensions import NotRequired, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ConsolidationState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    session_id: NotRequired[int]
    document_id: NotRequired[int]
    class_name: NotRequired[str]
    learning_objectives: NotRequired[list[str]]
    questions: NotRequired[list[dict[str, Any]]]
    current_index: NotRequired[int]
    answers: NotRequired[list[dict[str, Any]]]
    report: NotRequired[Optional[dict[str, Any]]]
