# Will chat with user
import json
from typing import AsyncIterable, Iterable
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.services.agents.gemini_chat_agent.nodes.extraction_agent import (
    extraction_agent,
)
from src.services.agents.gemini_chat_agent.nodes.extract_missing_informations import (
    extract_missing_informations,
)
from src.services.agents.gemini_chat_agent.nodes.post_extraction_agent import (
    post_extraction_agent,
)


graph = StateGraph(AgentState)

graph.add_node("extract_missing_informations", extract_missing_informations)
graph.add_node("extraction_agent", extraction_agent)
graph.add_node("post_extraction_agent", post_extraction_agent)

graph.set_entry_point("extract_missing_informations")


def extract_missing_informations_router(state: AgentState):
    if state["missing_informations_to_extract"]:
        return "extraction_agent"
    else:
        return "post_extraction_agent"


graph.add_conditional_edges(
    "extract_missing_informations",
    extract_missing_informations_router,
    {
        "extraction_agent": "extraction_agent",
        "post_extraction_agent": "post_extraction_agent",
    },
)

graph.add_edge("extraction_agent", END)
graph.add_edge("post_extraction_agent", END)

runnable = graph.compile()


async def arun(user_message: str, er_visit_id: str) -> AsyncIterable[str]:
    from src.services.agents.gemini_chat_agent.states.index import AgentState
    from src.datasources.prisma import prisma
    import jsonpickle
    
    await prisma.connect()
    # create erVisitId if there's none
    db_ervisit = await prisma.ervisit.upsert(
        where={"id": er_visit_id},
        data={"create": {"id": er_visit_id}, "update": {}},
        include={"ChatMessages": {"take": 4, "order_by": {"createdAt": "desc"}}},
    )
    prev_messages = db_ervisit.ChatMessages or []
    prev_messages.reverse()
    parsed_prev_messages = []
    for message in prev_messages:
        print("raw", message.raw)
        parsed_prev_messages.append(jsonpickle.decode(message.raw))

    input = {
        "messages": parsed_prev_messages,
        "input_messages": [HumanMessage(content=user_message)],
        "er_visit_id": er_visit_id,
    }

    # # not streaming
    # final_state: AgentState = AgentState()
    # async for output in runnable.astream(inputs, debug=True):
    #     # stream() yields dictionaries with output keyed by node name
    #     for key, value in output.items():
    #         print(f"Output from node '{key}':")
    #         print("---")
    #         print(value)
    #         final_state = value
    #     print("\n---\n")

    # # # save to db
    # res1 = await prisma.chatmessage.create(
    #     data={
    #         "erVisitId": er_visit_id,
    #         "raw": jsonpickle.encode(final_state["input_messages"][0]),
    #     }
    # )
    # print("res1", res1)
    # res2 = await prisma.chatmessage.create(
    #     data={
    #         "erVisitId": er_visit_id,
    #         "raw": jsonpickle.encode(final_state["final_messages"][0]),
    #     }
    # )
    # print("res2", res2)
    # await prisma.disconnect()
    # return final_state
    # TODO: refactor !
    # TODO: make it streamable

    stream = runnable.astream_log(input=input)
    final_text = ""
    async for output in stream:
        # print("output", output.ops)
        # print("\n")
        for op in output.ops:
            # print("op", op)
            if op["path"].startswith("/logs/ChatGoogleGenerativeAI/streamed_output_str/-"):
                final_text += op["value"]
                yield op["value"]
                # print("stream",op["value"])
            elif op["path"].startswith("/logs/") and op["path"].endswith(
                "/streamed_output/-"
            ):
                # because we chose to only include LLMs, these are LLM tokens
                # print("streamed_output", op["value"])
                pass
    # # save to db
    res1 = await prisma.chatmessage.create(
        data={
            "erVisitId": er_visit_id,
            "raw": jsonpickle.encode(input["input_messages"][0]),
        }
    )
    print("res1", res1)
    res2 = await prisma.chatmessage.create(
        data={
            "erVisitId": er_visit_id,
            "raw": jsonpickle.encode(AIMessage(content=final_text)),
        }
    )
    
    await prisma.disconnect()