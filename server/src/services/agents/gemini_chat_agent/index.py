# Will chat with user
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.services.agents.gemini_chat_agent.nodes.extraction_agent import (
    extraction_agent,
)
from src.services.agents.gemini_chat_agent.nodes.extract_missing_informations import (
    extract_missing_informations,
)
from src.services.agents.gemini_chat_agent.nodes.after_extraction_agent import (
    after_extraction_agent,
)

graph = StateGraph(AgentState)

graph.add_node("extract_missing_informations", extract_missing_informations)
graph.add_node("extraction_agent", extraction_agent)
graph.add_node("after_extraction_agent", after_extraction_agent)

graph.set_entry_point("extract_missing_informations")


def extract_missing_informations_router(state: AgentState):
    if state["missing_information_to_extract"]:
        return "extraction_agent"
    else:
        return "after_extraction_agent"


graph.add_conditional_edges(
    "extract_missing_informations",
    extract_missing_informations_router,
    {
        "extraction_agent": "extraction_agent",
        "after_extraction_agent": "after_extraction_agent",
    },
)
graph.add_edge("extraction_agent", END)
graph.add_edge("after_extraction_agent", END)

runnable = graph.compile()


async def arun(user_message: str, user_id: str):
    # TODO: bypass user id from agent tool call for security
    inputs = {"messages": [HumanMessage(content=user_message)], "user_id": user_id}

    # not streaming
    async for output in runnable.astream(inputs,debug=True):
        # stream() yields dictionaries with output keyed by node name
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")
    # count = 0
    # async for output in runnable.astream_log(inputs, include_types=["llm"]):
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
