from src.datasources.prisma import prisma
from nest_asyncio import apply
apply()



async def astream():
    from src.services.agents.gemini_chat_agent.index import arun
    await prisma.connect()
    
    user_message = """hello my name is Osama, i am 40 amd my bp is 80 120, i don't know my body temp, i arrive here 
    by Grab, my heart rate seems normal, my oxygen is 99%. I have an injury in my leg and my breathing is tight. 
    My pain is about 8 out of 10. Temperature is 38 and I feel diziness and chest paint"""

    await arun(user_message=user_message, er_visit_id="test")
    await prisma.disconnect()


import asyncio

asyncio.run(astream())

