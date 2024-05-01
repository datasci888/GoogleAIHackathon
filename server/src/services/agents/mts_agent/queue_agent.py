from datetime import datetime
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from src.configs.index import GOOGLE_API_KEY
from src.services.agents.mts_agent.state import AgentState
from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from src.services.agents.tools import save_patient_triage_colour, save_patient_info_kg
from langchain_core.messages import AIMessage, HumanMessage
from src.datasources.prisma import prisma
from src.utils.knowledge_graph import KnowledgeGraph


async def astream(state: AgentState):
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    today_datetime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    runnable = create_function_calling_executor(
        model=model, tools=[save_patient_info_kg.tool, save_patient_triage_colour.tool]
    )

    kg = KnowledgeGraph(label=state["er_visit_id"], verbose=True)

    # TODO cache and asyncio gather
    patient_info = await kg.aquery_knowledge(
        query="""find all information about the patient"""
    )

    patient_symptoms_and_classification = await prisma.erpatientrecord.find_first(
        where={"erVisitId": state["er_visit_id"]}
    )

    async_stream = runnable.astream(
        input={
            "messages": [
                HumanMessage(
                    content=f"""Let's think step by step.
                    Today time is : {today_datetime}
                    You are a ER Triage Agent.
                    Monitor and gather more information about patient's medical data.
                    
                    The Manchester Triage System (MTS) is a method used in some emergency departments in the United Kingdom and other healthcare settings worldwide to prioritize patients based on the urgency of their medical needs. It helps ensure that patients who need the most urgent care are seen first. The system classifies patients into five different levels of urgency, each represented by a specific color:
                    1. Red (Immediate): Life-threatening conditions that require immediate treatment within minutes. Examples include cardiac arrest, severe respiratory distress, or major trauma.
                    2. Orange (Very Urgent): Serious conditions that require very urgent attention within 10 minutes. Conditions might include severe pain, active hemorrhage not controlled by simple measures, or high-risk chest pain.
                    3. Yellow (Urgent): Urgent but not immediately life-threatening conditions that should be seen within 60 minutes. Examples could be moderate asthma, abdominal pain, or a high fever in children.
                    4. Green (Standard): Less urgent cases where the patient needs to be seen within 120 minutes. These might include minor injuries and illnesses such as sprains or a cold.
                    5. Blue (Non-Urgent): Non-urgent cases where the patient can typically wait to be seen, usually within 240 minutes. Examples include chronic issues without acute worsening, or minor symptoms like a cough or sore throat.

                    Here's information about the patient:
                    er_visit_id: {state['er_visit_id']}
                    
                    {patient_info.response}
                    
                    {patient_symptoms_and_classification.model_dump_json(exclude_none=True)}
                    
                    Here's previous conversation history:
                    {json.dumps(state['messages'] + [HumanMessage(content=state["input_text"])], default=str)}
                    """
                )
            ]
        }
    )

    state["output_stream"] = async_stream
    return state
