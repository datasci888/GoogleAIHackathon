from typing import AsyncIterator, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.messages.base import BaseMessageChunk


class AgentState(TypedDict):
    messages: list[BaseMessage] = []
    er_visit_id: str
    input_text: str
    output_stream: AsyncIterator[BaseMessageChunk] | None
    review: dict | None