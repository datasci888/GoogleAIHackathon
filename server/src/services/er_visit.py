from typing import Annotated
from pydantic import Field
from prisma.models import ERVisit as PrismaERVisit
from prisma.types import ERVisitCreateInput, ERVisitUpdateInput


class ERVisit(PrismaERVisit):
    def __init__(
        self, id: Annotated[str | None, Field(description="erVisitId")] = None
    ):
        self.id = id
        pass

    async def aload(self):
        from src.datasources.prisma import prisma

        data = await prisma.ervisit.find_first(where={"id": self.id})

        if data:
            data = data.model_dump()

            for key, value in data.items():
                setattr(self, key, value)

    async def asave(self):
        from src.datasources.prisma import prisma

        data = self.model_dump(exclude_defaults=True)
        data = await prisma.ervisit.upsert(
            where={"id": self.id},
            data={
                "create": ERVisitCreateInput(**data),
                "update": ERVisitUpdateInput(**data),
            },
        )

        if data:
            data = data.model_dump()

            for key, value in data.items():
                setattr(self, key, value)
