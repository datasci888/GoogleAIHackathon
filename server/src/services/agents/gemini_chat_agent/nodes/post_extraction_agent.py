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
            content=f"""You are a Triage Assistant.
                        here's the patient temporary queue number
                        this queue number is calculated in real time
                        {queue_number}
                        today time is : {today_datetime}
                        user_id is: {state["user_id"]}
                        """
        ),
        AIMessage(content="Understood"),
    ]
    response = await gemini_agent.ainvoke(
        input={"messages": SYSTEM_PROMPT + state["messages"]}
    )

    state["messages"] = [response]
    return state