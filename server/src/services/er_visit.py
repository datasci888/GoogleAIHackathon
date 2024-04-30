from typing import Annotated


async def read_er_visit(id: Annotated[str, Field(description="ER visit ID / session id, unique per user")]):
    from src.datasources.prisma import prisma

    db_er_visit = await prisma.ervisit.find_unique(where={"id": id})

    return db_er_visit
