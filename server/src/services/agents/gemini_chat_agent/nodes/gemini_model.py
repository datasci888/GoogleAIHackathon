from typing import Literal
from src.configs.index import GOOGLE_API_KEY
from src.services.agents.gemini_chat_agent.states.index import AgentState
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

async def gemini_model(state: AgentState):
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

    input = [
        HumanMessage(
            content="""You are a Triage assistant
                     """
        ),
        AIMessage(content="understood"),
    ] + state["input_messages"]

    response = await  model.astream(input=input)
    state["messages"] = response
    return state


from langgraph.graph import StateGraph, END


graph = StateGraph(AgentState)

graph.add_node("gemini_model", gemini_model)

graph.add_edge("gemini_model", END)

graph.set_entry_point("gemini_model")
runnable = graph.compile()

async def run():
    # streaming = await runnable.ainvoke(input={"input_messages": [HumanMessage(content="hello")]}, debug=True)
    # print("streaming", streaming)
    
    streaming = runnable.astream_log(input={"input_messages": [HumanMessage(content="hello what is MTS ?")]})

    final_text = ""
    async for output in streaming:
        # print("output", output.ops)
        # print("\n")
        for op in output.ops:
            # print("op", op)
            if op["path"].startswith("/logs/ChatGoogleGenerativeAI/streamed_output_str/-"):
                final_text += op["value"]
                yield op["value"]
                print("stream",op["value"])
            elif op["path"].startswith("/logs/") and op["path"].endswith(
                "/streamed_output/-"
            ):
                # because we chose to only include LLMs, these are LLM tokens
                # print("streamed_output", op["value"])
                pass
    print("funal", final_text)

import asyncio

async def test():
    stream = run()
    async for output in stream:
        print(output)
        
asyncio.run(test())