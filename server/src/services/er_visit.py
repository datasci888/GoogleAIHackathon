async def read_er_visit(id: str):
    from src.datasources.prisma import prisma

    db_er_visit = await prisma.ervisit.find_unique(
        where={"id": id},
        include={"ChatMessages": {"order_by": {"createdAt": "desc"}, "take": 20}},
    )

    return db_er_visit
