import json
from typing import List
import jsonpickle
from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from src.configs.index import GOOGLE_API_KEY
from langchain_core.messages import HumanMessage, AIMessage
from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.services.agents.tools.save_patient_info import save_patient_info_tool
from datetime import datetime
from src.datasources.prisma import prisma
from prisma.types import ChatMessageCreateWithoutRelationsInput
from langchain_core.messages import BaseMessage, FunctionMessage, AIMessage
import pickle

async def extraction_agent(state: AgentState):
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    gemini_agent = create_function_calling_executor(
        model=model, tools=[save_patient_info_tool]
    )
    today_datetime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    missing_informations_to_extract = state["missing_information_to_extract"]

    SYSTEM_PROMPT = [
        HumanMessage(
            content=f"""You are a Triage Assistant.
                        Your task is to retrieve information to ensure that the patient is well treated.
                        
                        Here are the information that you need to ask and save :
                        {json.dumps(missing_informations_to_extract)}
                        today time is : {today_datetime}
                        er_visit_id is: {state["er_visit_id"]}
                        
                        After saving the information, sympathetize with the patient and request for the remaining missing information from the user.
                        """
        ),
        AIMessage(content="Understood"),
    ]
    
    # dynamically add a filler message
    if isinstance(state["messages"][0],AIMessage):
        SYSTEM_PROMPT.append(HumanMessage(content="hmm"))
        
    messages = SYSTEM_PROMPT + state["messages"]

    response = await gemini_agent.ainvoke(
        input={"messages":messages}
    )
    state["messages"] = state["messages"] + [response["messages"][-1]]

    # # save to db
    for message in state["messages"]:
        message : BaseMessage
        print("message",message)
        # we skip if it's function message or function call
        if isinstance(message, FunctionMessage):
            continue
        if isinstance(message, AIMessage) and message.content == "":
            continue
        print("message2",message)
        await prisma.chatmessage.create(
            data={"raw": jsonpickle.encode(message), "erVisitId": state["er_visit_id"]},
        )

    return state
