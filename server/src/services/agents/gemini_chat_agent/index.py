# Will chat with user
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from nest_asyncio import apply
apply()
from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.services.agents.gemini_chat_agent.nodes.gemini_chat_agent import gemini_chat_agent
from src.datasources.prisma import prisma
graph = StateGraph(AgentState)

graph.add_node("router", gemini_chat_agent)
graph.set_entry_point("router")
graph.add_edge("router", END)

runnable = graph.compile()


import asyncio


async def run(user_message: str, user_id: str):
    # TODO: bypass user id from agent tool call for security
    inputs = {"messages": [HumanMessage(content=user_message)], "user_id": user_id}
    await prisma.connect()
    async for output in runnable.astream(inputs):
        # stream() yields dictionaries with output keyed by node name
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")

    await prisma.disconnect()

asyncio.run(run(user_id="test", user_message="hello my name is viky, my bp is 80 120, i don't know my body temp, i arrive here by Grab, my heart rate seems normal, my oxygen is 99%"))
