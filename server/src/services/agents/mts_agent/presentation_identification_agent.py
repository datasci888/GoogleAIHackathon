import json
from src.configs.index import GOOGLE_API_KEY
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

    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

    runnable = create_function_calling_executor(
        model=model,
        tools=[save_patient_presenting_complaint.tool, save_patient_info_kg.tool],
    )

    response = runnable.astream(
        input={
            "messages": [
                HumanMessage(
                    content=f"""Let's think step by step.
                You are a Triage assistant in charge of ER Triage.
                Your task is to identify the most likely presenting symptom experienced by the patient and record it using tool.
                Ask the patient's chief complaint or description of their issue.
                er_visit_id: {state['er_visit_id']}
                
                Here's previous conversation history:
                {json.dumps(state['messages'] +[HumanMessage(content=state["input_text"])], default=str)}"""
                ),
            ]
        }
    )

    # state["messages"] += [HumanMessage(content=state["input_text"]), AIMessage(content="understood")]
    state["output_stream"] = response
    return state
