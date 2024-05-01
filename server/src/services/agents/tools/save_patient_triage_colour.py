from typing import Annotated, Literal
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field


async def arun(
    er_visit_id: Annotated[str, Field(description="erVisitId")],
    triage_classification_colour: Annotated[
        Literal["RED", "ORANGE", "YELLOW", "GREEN", "BLUE"],
        Field(description="Most likely classification colour"),
    ],
):
    from src.datasources.prisma import prisma

    try:
        db_patientrecord = await prisma.erpatientrecord.update(
            where={"erVisitId": er_visit_id},
            data={"triageColour": triage_classification_colour},
        )

        return db_patientrecord.model_dump_json()
    except Exception as e:
        raise ToolException(str(e))


tool = StructuredTool.from_function(
    name="save_patient_triage_classification_colour",
    description="use this to save patient colour classification",
    coroutine=arun,
    handle_tool_error=True,
)
