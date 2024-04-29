from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from langchain_google_genai import ChatGoogleGenerativeAI
from src.configs.index import GOOGLE_API_KEY
from langchain_core.messages import HumanMessage, AIMessage
from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.services.agents.tools.save_patient_info import save_patient_info_tool
from datetime import datetime



async def post_extraction_agent(state: AgentState):
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

    gemini_agent = create_function_calling_executor(
        model=model, tools=[save_patient_info_tool]
    )

    today_datetime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


    # TODO retrieve triage classification, and queue number from db, and assist user for information
    triage_classification = "urgent"

    
    # TODO query user queue number
    queue_number = "1"
    
    # TODO do some RAG ?
    # TODO equip with RAG tool ?
    # TODO equip with contact medic tool ?
    # TODO retrieve chat history from db ?
    SYSTEM_PROMPT = [
        HumanMessage(
            content=f"""You are an expert triage and emergency nurse who is responsile for classifying 
                        the triage level of the patient based on the collected inputs and below context:
                        {state["messages"]}

                        Based on the provided details for this patient, you have to follow Manchester Triage System (MTS)  
                        to classify the urgency level. 

                        The Manchester Triage System (MTS) is a method used in some emergency departments in the United Kingdom and other healthcare settings worldwide to prioritize patients based on the urgency of their medical needs. It helps ensure that patients who need the most urgent care are seen first. The system classifies patients into five different levels of urgency, each represented by a specific color:
                        1. Red (Immediate): Life-threatening conditions that require immediate treatment within minutes. Examples include cardiac arrest, severe respiratory distress, or major trauma.
                        2. Orange (Very Urgent): Serious conditions that require very urgent attention within 10 minutes. Conditions might include severe pain, active hemorrhage not controlled by simple measures, or high-risk chest pain.
                        3. Yellow (Urgent): Urgent but not immediately life-threatening conditions that should be seen within 60 minutes. Examples could be moderate asthma, abdominal pain, or a high fever in children.
                        4. Green (Standard): Less urgent cases where the patient needs to be seen within 120 minutes. These might include minor injuries and illnesses such as sprains or a cold.
                        5. Blue (Non-Urgent): Non-urgent cases where the patient can typically wait to be seen, usually within 240 minutes. Examples include chronic issues without acute worsening, or minor symptoms like a cough or sore throat.

                        here's the patient temporary queue number
                        this queue number is calculated in real time
                        {queue_number}
                        today time is : {today_datetime}
                        user_id is: {state["user_id"] if "user_id" in state else "Unknown"}

                        Your final answer should be the triage classification (one of the five MTS levels) with supporting reasons from the provided context.

                        Answer:
                        """
        ),
        AIMessage(content="Understood"),
    ]
    response = await gemini_agent.ainvoke(
        input={"messages": SYSTEM_PROMPT + state["messages"]}
    )

    state["messages"] = [response]
    return state