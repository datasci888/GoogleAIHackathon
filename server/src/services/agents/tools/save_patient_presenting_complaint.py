from typing import Annotated, Literal
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field
from src.utils.knowledge_graph import KnowledgeGraph
from src.datasources.prisma import prisma
import asyncio


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
        ],
        Field(description="Choose one of patient presenting symptom"),
    ],
):
    """Save patient presenting symptom"""

    try:
        kg = KnowledgeGraph(label=er_visit_id, verbose=True)

        await asyncio.gather(
            prisma.erpatientrecord.upsert(
                where={"erVisitId": er_visit_id},
                data={
                    "create": {
                        "chiefComplaint": presenting_symptom,
                        "erVisitId": er_visit_id,
                    },
                    "update": {"chiefComplaint": presenting_symptom},
                },
            ),
            kg.astore_knowledge(
                knowledge=f"patient presenting symptom is {presenting_symptom}"
            ),
        )

        return f"{presenting_symptom} has been recorded"
    except Exception as e:
        raise ToolException(str(e))


tool = StructuredTool.from_function(
    name="save_patient_presenting_symptom",
    description="use this to save patient presenting symptom",
    coroutine=arun,
    handle_tool_error=True,
)
