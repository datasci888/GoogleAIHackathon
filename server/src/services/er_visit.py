async def read_er_visit(id: str):
    from src.datasources.prisma import prisma

    db_er_visit = await prisma.ervisit.find_unique(
        where={"id": id},
        include={"ChatMessages": {"order_by": {"createdAt": "desc"}, "take": 10}},
    )

    if not db_er_visit:
        db_er_visit = await prisma.ervisit.create(
            data={"id": id},
            include={
                "ChatMessages": {"order_by": {"createdAt": "desc"}, "take": 10}
            },
        )
    return db_er_visit

