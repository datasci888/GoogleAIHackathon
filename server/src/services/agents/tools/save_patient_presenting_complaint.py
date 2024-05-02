from typing import Annotated, Literal
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field


async def arun(
    er_visit_id: Annotated[str, Field(description="erVisitId")],
    presenting_symptom: Annotated[
        Literal[
            "Abdominal pain in adults",
            "Abdominal pain in children",
            "Abscesses and local infections",
            "Allergy",
            "Apparently drunk",
            "Assault",
            "Asthma",
            "Back pain",
            "Behaving strangely",
            "Bites and stings",
            "Burns and scalds",
            "Chest pain",
            "Collapsed adult",
            "Crying baby",
            "Dental problems",
            "Diabetes",
            "Diarrhoea and vomiting",
            "Ear problems",
            "Exposure to chemicals",
            "Eye problems",
            "Facial problems",
            "Falls",
            "Fits",
            "Foreign body",
            "GI bleeding",
            "Headache",
            "Head injury",
            "Irritable child",
            "Limb problems",
            "Limping child",
            "Major trauma",
            "Mental illness",
            "Neck pain",
            "Overdose and poisoning",
            "Palpitations",
            "Pregnancy",
            "PV bleeding",
            "Rashes",
            "Self-harm",
            "Sexually acquired infection",
            "Shortness of breath in adults",
            "Shortness of breath in children",
            "Sore throat",
            "Testicular pain",
            "Torso injury",
            "Unwell adult",
            "Unwell child",
            "Urinary problems",
            "Worried parent",
            "Wounds",
            None,
        ],
        Field(description="Patient presenting symptom"),
    ] = None,
):
    from src.datasources.prisma import prisma

    if not presenting_symptom:
        return None
    try:
        db_patientrecord = await prisma.erpatientrecord.upsert(
            where={"erVisitId": er_visit_id},
            data={
                "create": {
                    "chiefComplaint": presenting_symptom,
                    "erVisitId": er_visit_id,
                },
                "update": {"chiefComplaint": presenting_symptom},
            },
        )
        from src.utils.knowledge_graph import KnowledgeGraph

        kg = KnowledgeGraph(label=er_visit_id, verbose=True)
        await kg.astore_knowledge(
            knowledge=f"patient presenting symptom is {presenting_symptom}"
        )
        return db_patientrecord.model_dump_json()
    except Exception as e:
        raise ToolException(str(e))


tool = StructuredTool.from_function(
    name="save_patient_presenting_symptom",
    description="use this to save patient presenting symptom",
    coroutine=arun,
    handle_tool_error=True,
)
