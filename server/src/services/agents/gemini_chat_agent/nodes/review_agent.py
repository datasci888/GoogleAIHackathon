from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from src.configs.index import GOOGLE_API_KEY
from src.services.agents.gemini_chat_agent.states.index import AgentState


async def review_agent(state: AgentState):
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    
    class Review(BaseModel):
        """Review"""
        review: str
        accuracy: int
        coherency: int
    
    runnable = model.with_structured_output(schema=Review)
    
    
    review : Review = await runnable.ainvoke(input=f"""
                                             Let's think step by step.
                                             Given a original message and response message, submit a review.
                                             Every review score should be between 0 to 5.
                                             
                                             [Original Message]: 
                                             {state['input_message'].content}
                                             
                                             [Response Message]: 
                                             {state['final_message'].content}
                                             """)
    state["review_message"] = review.model_dump()

    return state