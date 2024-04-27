from src.datasources.prisma import prisma
from nest_asyncio import apply
apply()



async def astream():
    from src.services.agents.gemini_chat_agent.index import arun
    await prisma.connect()
    
    await arun(user_message="hi", user_id="test")
    await prisma.disconnect()


import asyncio

asyncio.run(astream())

