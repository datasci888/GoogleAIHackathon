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

    missing_informations_to_extract = state["missing_informations_to_extract"]

    examples = [{
  "sex": "male",
  "arrival_mode": "private car",
  "age": "40",
  "blood_pressure": "80/120",
  "oxygen_saturation": "99%",
  "chief_complaint": "chest pain since morning with itiching in my body.",
  "user_id": "test",
  "mental_state": "normal",
  "pain_intensity": "7",
  "heart_rate": "115",
  "respiratory_rate": "normal",
  "injury": "I have minor injury in my neck",
  "body_temperature": "38"
}
]
    
    SYSTEM_PROMPT = [
        HumanMessage(
            content = f"""You are a Triage Assistant.
                        Your only task is to retrieve information to ensure that the patient is well treated.
                        Do not be chatty or do not ask any more questions if the required details in below are captured 
                        from the given user prompt. 
                        If the chief complaint is not mentioned explicity by the patient, check if his complaint is mentioned in the provided context.
                        Here are the information that you need to ask
                         {json.dumps(missing_informations_to_extract)}
                        today time is : {today_datetime}
                        er_visit_id is: {state["er_visit_id"]}
                        Here are also example for what you suppose to capture from the user's inputs:
                        {examples}

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
