from nest_asyncio import apply
apply()



async def astream():
    from src.services.agents.mts_agent.index import astream
    
    async for chunk in astream("test5", "i have shortness of breath"):
        print(chunk)

import asyncio

asyncio.run(astream())

