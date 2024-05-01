from typing import Sequence, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    er_visit_id: str
    missing_informations_to_extract: list[str] | None = None
    input_message: BaseMessage | None = None
    final_message: BaseMessage | None = None
    review: dict