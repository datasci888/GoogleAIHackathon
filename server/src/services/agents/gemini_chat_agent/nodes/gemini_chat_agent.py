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


async def gemini_chat_agent(state: AgentState):
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    gemini_agent = create_function_calling_executor(
        model=model, tools=[save_patient_info_tool]
    )
    today_datetime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # retrieve missing information to extract from db

    db_patient = await prisma.patientrecord.find_first(
        where={"userId": state["user_id"]}
    )

    if not db_patient:
        db_patient = await prisma.patientrecord.create(
            data={
                "userId": state["user_id"],
            }
        )

    missing_informations_to_extract = []

    for key, value in db_patient.model_dump().items():
        if value is None:
            missing_informations_to_extract.append(key)

    SYSTEM_PROMPT = [HumanMessage(
            content=f"""You are a Triage Assistant.
                        Your task is to retrieve information to ensure that the patient is well treated.
                        Here are the information that you need to ask
                        {json.dumps(missing_informations_to_extract)}
                        today time is : {today_datetime}
                        user_id is: {state["user_id"]}
                        """
        ), AIMessage(content="Understood")]
    response = await gemini_agent.ainvoke(
        input={"messages": SYSTEM_PROMPT + state["messages"]}
    )

    state["messages"] = [response]
    return state
