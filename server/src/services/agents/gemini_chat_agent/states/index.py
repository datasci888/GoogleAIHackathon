import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    er_visit_id: str
    missing_informations_to_extract: list[str] | None = None