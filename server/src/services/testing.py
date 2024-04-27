import json
from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from src.configs.index import GOOGLE_API_KEY
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.services.agents.tools.save_patient_info import save_patient_info_tool
from datetime import datetime
from src.datasources.prisma import prisma


async def astream():
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    gemini_agent = create_function_calling_executor(
        model=model, tools=[save_patient_info_tool]
    )
    
    stream = gemini_agent.astream(input={"messages": [HumanMessage(content="hello")], "user_id": "test"}, stream_mode="updates")
    
    async for output in stream:
        print(output)


import asyncio

asyncio.run(astream())

