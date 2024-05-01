from typing import AsyncIterable
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
    "presentation_identification_agent", presentation_identification_agent.astream
)
graph.add_node("discriminators_agent", discriminators_agent.astream)
graph.add_node("queue_agent", queue_agent.astream)


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


async def astream(er_visit_id: str, input_text: str) -> AsyncIterable[str]:
    await prisma.connect()
    
    # retrieve previous messages
    db_chat_messages = await prisma.chatmessage.find_many(
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
    
    
    astream = runnable.astream(
        input=AgentState({"er_visit_id": er_visit_id, "input_text": input_text,"messages":messages}),
        debug=True,
    )

    final_text = ""
    async for chunk in astream:
        for key in chunk:
            state: AgentState = chunk[key]
        # print("state", state)
        if state.get("output_stream",[]):
            # print("output_stream", state["output_stream"])
            async for schunk in state["output_stream"]:
                print("schunk", schunk)
                text_chunk = ""
                if "agent" in schunk:
                    text_chunk = schunk["agent"]["messages"][0].content
                elif "action" in schunk:
                    # function call
                    text_chunk = schunk["action"]["messages"][0].content
                yield text_chunk
                final_text += text_chunk

    # store in db
    db_user_chatmessage = await prisma.chatmessage.create(
        data={
            "erVisitId": er_visit_id,
            "raw": jsonpickle.encode(HumanMessage(content=input_text)),
        }
    )
    db_ai_chatmessage = await prisma.chatmessage.create(
        data={
            "erVisitId": er_visit_id,
            "raw": jsonpickle.encode(AIMessage(content=final_text)),
        }
    )

    await prisma.disconnect()
