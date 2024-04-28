from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.datasources.prisma import prisma


async def extract_missing_informations(state: AgentState):
    # create erVisitId if there's none
    db_ervisit = await prisma.ervisit.upsert(
        where={"id": state["er_visit_id"]},
        data={"create": {"id": state["er_visit_id"]}, "update": {}},
    )

    # retrieve missing information to extract from db
    db_erpatientrecord = await prisma.erpatientrecord.find_first(
        where={"erVisitId": state["er_visit_id"]}
    )

    print("db_erpatientrecord", db_erpatientrecord)
    if not db_erpatientrecord:
        db_erpatientrecord = await prisma.erpatientrecord.create(
            data={"erVisitId": state["er_visit_id"]}
        )
    
    print("db_erpatientrecord", db_erpatientrecord)
    missing_informations_to_extract = []

    print("state", state)
    for key, value in db_erpatientrecord.model_dump().items():
        if value is None:
            missing_informations_to_extract.append(key)

    state["missing_information_to_extract"] = missing_informations_to_extract
    state["messages"] = []
    return state
