from typing import AsyncIterable, Iterable
from langgraph.graph import StateGraph, END
from src.services.agents.mts_agent.conditional_entry import conditional_entry
from src.services.agents.mts_agent.state import AgentState
from src.services.agents.mts_agent import (
    presentation_identification_agent,
    discriminators_agent,
    queue_agent,
)
from langchain_core.messages import AIMessage, HumanMessage
import jsonpickle
from src.datasources.prisma import prisma

graph = StateGraph(AgentState)

graph.add_node(
    "presentation_identification_agent", presentation_identification_agent.stream
)
graph.add_node("discriminators_agent", discriminators_agent.stream)
graph.add_node("queue_agent", queue_agent.stream)


graph.set_conditional_entry_point(
    condition=conditional_entry,
    conditional_edge_mapping={
        "presentation_identification_agent": "presentation_identification_agent",
        "discriminators_agent": "discriminators_agent",
        "queue_agent": "queue_agent",
    },
)

graph.add_edge("presentation_identification_agent", END)
graph.add_edge("discriminators_agent", END)
graph.add_edge("queue_agent", END)

runnable = graph.compile()


def stream(
    er_visit_id: str, input_text: str | None, input_image: bytes | None = None
) -> Iterable[str]:

    # retrieve previous messages
    db_chat_messages = prisma.chatmessage.find_many(
        where={"erVisitId": er_visit_id},
        order={"createdAt": "desc"},
        take=4,
    )

    # parse and reverse
    messages = []
    index = len(db_chat_messages) - 1
    while index >= 0:
        messages.append(jsonpickle.decode(db_chat_messages[index].raw))
        index -= 1

    stream = runnable.stream(
        input=AgentState(
            {"er_visit_id": er_visit_id, "input_text": input_text, "messages": messages}
        ),
        debug=True,
    )

    final_text = ""
    for chunk in stream:
        for key in chunk:
            state: AgentState = chunk[key]
        # print("state", state)
        if state.get("output_stream", []):
            # print("output_stream", state["output_stream"])
            for schunk in state["output_stream"]:
                if "agent" in schunk:
                    text_chunk = schunk["agent"]["messages"][0].content
                    if text_chunk:
                        final_text += text_chunk
                elif "action" in schunk:
                    action_chunk = schunk["action"]["messages"][0].content
                    if action_chunk:
                        # function call
                        final_text += action_chunk
            yield final_text

    # store in db
    db_user_chatmessage = prisma.chatmessage.create(
        data={
            "erVisitId": er_visit_id,
            "raw": jsonpickle.encode(HumanMessage(content=input_text)),
        }
    )
    db_ai_chatmessage = prisma.chatmessage.create(
        data={
            "erVisitId": er_visit_id,
            "raw": jsonpickle.encode(AIMessage(content=final_text)),
        }
    )
