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


async def astream(state: AgentState):
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

    db_erpatientrecord = await prisma.erpatientrecord.find_first(
        where={"erVisitId": state["er_visit_id"]}
    )

    if not db_erpatientrecord:
        raise HTTPException(
            status_code=INTERNAL_SERVER_ERROR,
            detail="ERPatientRecord not found, impossible path",
        )

    print("db_erpatientrecord", db_erpatientrecord)
    # TODO: do asyncio gather

    kg = KnowledgeGraph(label=state["er_visit_id"], verbose=True)

    discriminators_context, patient_info = await asyncio.gather(
        discriminators_knowledge_retrieval.aquery(
            query=db_erpatientrecord.chiefComplaint,
        ),
        kg.aquery_knowledge(query="""patient"""),
    )

    print("patient_info", patient_info)

    input = {
        "messages": (
            [
                HumanMessage(
                    content=f"""Let's think step by step.
                                You are a ER Triage agent, talking to the patient.
                                Classify the patient's triage Colour based on MTS and record it using tool.
                                If more information is needed, ask the patient's for additional symptoms or description of their issue.
                                
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

        async_stream = runnable.astream(input=input)

        state["output_stream"] = async_stream
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

        async_stream = runnable.astream(input=input)

        state["output_stream"] = async_stream
        return state
