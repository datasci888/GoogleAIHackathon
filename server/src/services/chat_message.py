from src.datasources.prisma import prisma
from 

class ChatMessage():
    def __init__(self, id: str | None = None) -> None:
        self.id = id
        pass
    
    async def aload(self):
        db_nessages = await prisma.chatmessage.find_unique(where={"id": self.id})
        pass
    
    async def asave(self):