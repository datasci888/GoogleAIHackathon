from src.services.agents.gemini_chat_agent.states.index import AgentState
from src.datasources.prisma import prisma


async def extract_missing_informations(state: AgentState):
    # retrieve missing information to extract from db
    db_erpatientrecord = await prisma.erpatientrecord.find_first(
        where={"erVisitId": state["er_visit_id"]}
    )

    if not db_erpatientrecord:
        db_erpatientrecord = await prisma.erpatientrecord.create(
            data={"erVisitId": state["er_visit_id"]}
        )

    missing_informations_to_extract = []

    for key, value in db_erpatientrecord.model_dump().items():
        if key == "erVisitId" or key == "ERVisit":
            continue
        if value is None:
            missing_informations_to_extract.append(key)

    state["missing_informations_to_extract"] = missing_informations_to_extract
    return state
