import json
from src.configs.index import GOOGLE_API_KEY, OPENAI_API_KEY
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from src.services.agents.mts_agent.state import AgentState
from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from src.services.agents.tools import (
    save_patient_presenting_complaint,
    save_patient_info_kg,
)


async def astream(state: AgentState):
    """
    Presentation Identification Agent
    - **Input**: Patient's chief complaint or description of their issue.
    - **Processing**:
      - Use a LangChain ConversationalRetrievalChain with a large language model (LLM) like Bard and a knowledge base of MTS presentations and their descriptions.
      - The LLM analyzes the input and retrieves the most likely MTS presentation category based on the knowledge base.
    - **Output**: Identified MTS presentation category (e.g., "Chest Pain").
    """
    input = {
        "messages": [
            HumanMessage(
                content=f"""Let's think step by step.
                    You are a Triage assistant in charge of ER Triage.
                    Ask the patient about what symptom they are experiencing. 
                    If no mention of presenting symptom, ask the patient for the symptom they are experiencing and how are they feeling.
                    Narrow down the possible presenting symptom to one of the following:
                        "Abdominal pain in adults",
                        "Abdominal pain in children",
                        "Abscesses and local infections",
                        "Allergy",
                        "Apparently drunk",
                        "Assault",
                        "Asthma",
                        "Back pain",
                        "Behaving strangely",
                        "Bites and stings",
                        "Burns and scalds",
                        "Chest pain",
                        "Collapsed adult",
                        "Crying baby",
                        "Dental problems",
                        "Diabetes",
                        "Diarrhoea and vomiting",
                        "Ear problems",
                        "Exposure to chemicals",
                        "Eye problems",
                        "Facial problems",
                        "Falls",
                        "Fits",
                        "Foreign body",
                        "GI bleeding",
                        "Headache",
                        "Head injury",
                        "Irritable child",
                        "Limb problems",
                        "Limping child",
                        "Major trauma",
                        "Mental illness",
                        "Neck pain",
                        "Overdose and poisoning",
                        "Palpitations",
                        "Pregnancy",
                        "PV bleeding",
                        "Rashes",
                        "Self-harm",
                        "Sexually acquired infection",
                        "Shortness of breath in adults",
                        "Shortness of breath in children",
                        "Sore throat",
                        "Testicular pain",
                        "Torso injury",
                        "Unwell adult",
                        "Unwell child",
                        "Urinary problems",
                        "Worried parent",
                        "Wounds",
                    Save using the presenting symptoms using tool after you narrow it down.
                    
                    er_visit_id: {state['er_visit_id']}
                    
                    Here's the conversation history:
                    {json.dumps(state['messages'], default=str)}"""
            ),
            AIMessage(content="understood"),
            HumanMessage(content=state["input_text"]),
        ]
    }
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest", google_api_key=GOOGLE_API_KEY
        )

        runnable = create_function_calling_executor(
            model=model,
            tools=[save_patient_presenting_complaint.tool, save_patient_info_kg.tool],
        )

        response = runnable.astream(input=input)

        # state["messages"] += [HumanMessage(content=state["input_text"]), AIMessage(content="understood")]
        state["output_stream"] = response
        return state
    except Exception as e:
        from langchain_community.llms.openai import OpenAI
        model = ChatGoogleGenerativeAI(
            model="gemini-pro", google_api_key=GOOGLE_API_KEY
        )

        # model = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4-turbo")
        
        runnable = create_function_calling_executor(
            model=model,
            tools=[save_patient_presenting_complaint.tool, save_patient_info_kg.tool],
        )

        response = runnable.astream(input=input)

        state["output_stream"] = response
        return state
