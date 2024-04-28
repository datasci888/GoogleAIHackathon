# Will chat with user
import json
from langchain_core.messages import HumanMessage
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
import jsonpickle

graph = StateGraph(AgentState)

graph.add_node("extract_missing_informations", extract_missing_informations)
graph.add_node("extraction_agent", extraction_agent)
graph.add_node("post_extraction_agent", post_extraction_agent)

graph.set_entry_point("extract_missing_informations")


def extract_missing_informations_router(state: AgentState):
    if state["missing_information_to_extract"]:
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


async def arun(user_message: str, er_visit_id: str):
    from src.services.agents.gemini_chat_agent.states.index import AgentState
    from src.datasources.prisma import prisma
    # create erVisitId if there's none
    db_ervisit = await prisma.ervisit.upsert(
        where={"id": er_visit_id},
        data={"create": {"id": er_visit_id}, "update": {}},
        include={"ChatMessages": {"take": 4,"order_by": {"createdAt": "desc"}}},
    )

    prev_messages = db_ervisit.ChatMessages or []
    prev_messages = prev_messages[::-1]
    parsed_prev_messages = []
    for message in prev_messages:
        parsed_prev_messages.append(
            jsonpickle.decode(message.raw)
        )
    
    print("prev_messages",parsed_prev_messages)
    
    messages = parsed_prev_messages + [HumanMessage(content=user_message)]
    inputs = {"messages": messages, "er_visit_id": er_visit_id}

    # not streaming
    async for output in runnable.astream(inputs):
        # stream() yields dictionaries with output keyed by node name
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")
    count = 0

    # async for output in runnable.astream_log(inputs, include_types=["llm"],debug=True):
    #     count += 1
    #     # astream_log() yields the requested logs (here LLMs) in JSONPatch format
    #     for op in output.ops:
    #         if op["path"] == "/streamed_output/-":
    #             # this is the output from .stream()
    #             ...
    #         elif op["path"].startswith("/logs/") and op["path"].endswith(
    #             "/streamed_output/-"
    #         ):
    #             # because we chose to only include LLMs, these are LLM tokens
    #             print("count", count)
    #             print(op["value"])
