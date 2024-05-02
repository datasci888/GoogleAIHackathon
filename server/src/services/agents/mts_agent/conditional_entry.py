from src.services.agents.mts_agent.state import AgentState


def conditional_entry(state: AgentState):
    from src.datasources.prisma import prisma

    db_ervisit = prisma.ervisit.upsert(
        where={"id": state["er_visit_id"]},
        data={"create": {"id": state["er_visit_id"]}, "update": {}},
        include={"ERPatientRecord": True},
    )

    print("db_ervisit", db_ervisit)

    if not db_ervisit.ERPatientRecord:
        return "presentation_identification_agent"
    elif not db_ervisit.ERPatientRecord.triageColour:
        return "discriminators_agent"
    else:
        return "queue_agent"
