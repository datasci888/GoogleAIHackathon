from datetime import datetime
from http.client import HTTPException, INTERNAL_SERVER_ERROR
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from src.configs.index import GOOGLE_API_KEY, OPENAI_API_KEY
from src.services.agents.mts_agent.state import AgentState
from src.datasources.prisma import prisma
from src.utils import discriminators_knowledge_retrieval
from langgraph.prebuilt.chat_agent_executor import create_function_calling_executor
from src.services.agents.tools import save_patient_info_kg, save_patient_triage_colour
from langchain_core.messages import HumanMessage, AIMessage
from src.utils.knowledge_graph import KnowledgeGraph
import asyncio


def stream(state: AgentState):
    """
    ### Discriminator Seeking Agent
    - **Input**: Identified MTS presentation category and potentially additional patient information.
    - **Processing**:
      - Access the corresponding MTS flow chart for the identified presentation.
      - Employ a LangChain LLMChain with an LLM to analyze the patient's information and answer the discriminator questions on the flow chart.
      - The LLM should be able to handle follow-up questions and gather necessary details.
    - **Output**: List of triggered discriminators (e.g., "Severe Pain", "Cardiac Pain").
    """
    # retrieve patient record
    today_datetime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    db_erpatientrecord = prisma.erpatientrecord.find_first(
        where={"erVisitId": state["er_visit_id"]}
    )

    if not db_erpatientrecord:
        raise HTTPException(
            status_code=INTERNAL_SERVER_ERROR,
            detail="ERPatientRecord not found, impossible path",
        )

    kg = KnowledgeGraph(label=state["er_visit_id"], verbose=True)

    discriminators_context = discriminators_knowledge_retrieval.query(
        query=db_erpatientrecord.chiefComplaint,
    )

    patient_info = kg.query_knowledge(query="""patient""")

    input = {
        "messages": (
            [
                HumanMessage(
                    content=f"""Let's think step by step.
                                Today time is : {today_datetime}
                                You are EVA an Emergency Virtual Assistant in charge of ER Triage.
                                You are talking to an ER patient.
                                Classify the patient's triage Colour based on MTS and record it using tool.
                                If more information is needed, ask the patient's for additional symptoms or description of their issue and record it using tool.
                                
                                Here's what we know about the patient:
                                {patient_info}
                                
                                And here's what we know about MTS discriminators:
                                {discriminators_context}
                                
                                er_visit_id: {state['er_visit_id']}
                                
                                Here's the conversation history:
                                {json.dumps(state['messages'], default=str)}
                                """
                ),
                AIMessage(content="understood"),
                HumanMessage(content=state["input_text"]),
            ]
        )
    }

    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest", google_api_key=GOOGLE_API_KEY
        )

        runnable = create_function_calling_executor(
            model=model,
            tools=[save_patient_info_kg.tool, save_patient_triage_colour.tool],
        )

        stream = runnable.stream(input=input)

        state["output_stream"] = stream
        return state
    except Exception as e:
        from langchain_community.llms.openai import OpenAI

        # model = ChatGoogleGenerativeAI(
        #     model="gemini-pro", google_api_key=GOOGLE_API_KEY
        # )
        model = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4-turbo")

        runnable = create_function_calling_executor(
            model=model,
            tools=[save_patient_info_kg.tool, save_patient_triage_colour.tool],
        )

        stream = runnable.stream(input=input)

        state["output_stream"] = stream
        return state
