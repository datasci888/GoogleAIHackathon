from typing import Annotated, Literal
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field


def run(
    er_visit_id: Annotated[str, Field(description="erVisitId")],
    triage_classification_colour: Annotated[
        Literal["RED", "ORANGE", "YELLOW", "GREEN", "BLUE"],
        Field(description="Most likely classification colour"),
    ],
):
    from src.datasources.prisma import prisma

    try:
        db_patientrecord = prisma.erpatientrecord.update(
            where={"erVisitId": er_visit_id},
            data={"triageColour": triage_classification_colour},
        )
        colour_hash = {
            "RED": "now.",
            "ORANGE": "within 10 minutes.",
            "YELLOW": "within 60 minutes.",
            "GREEN": "within 120 minutes.",
            "BLUE": "within 240 minutes.",
        }

        return f"""
```
Successfully queued at {db_patientrecord.updatedAt}
Expect a response {colour_hash[triage_classification_colour]}
Your queue code is {db_patientrecord.erVisitId}
```
"""
    except Exception as e:
        raise ToolException(str(e))


tool = StructuredTool.from_function(
    name="save_patient_triage_classification_colour",
    description="use this to save patient colour classification",
    func=run,
    handle_tool_error=True,
)
