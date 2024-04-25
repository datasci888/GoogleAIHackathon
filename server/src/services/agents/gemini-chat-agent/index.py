# Will chat with user
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from src.configs.index import GOOGLE_API_KEY
from langchain_core.messages import BaseMessage
from src.services.agents.tools.save_patient_info import save_patient_info_tool

model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
gemini_agent = create_function_calling_executor(
    model=model, tools=[TavilySearchResults(), save_patient_info_tool]
)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


graph = StateGraph(AgentState)

graph.add_node("router", gemini_agent)
graph.set_entry_point("router")
graph.add_edge("router", END)

runnable = graph.compile()

inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}

import asyncio


async def run():
    async for output in runnable.astream(inputs):
        # stream() yields dictionaries with output keyed by node name
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")


asyncio.run(run())
