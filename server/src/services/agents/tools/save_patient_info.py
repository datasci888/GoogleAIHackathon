from typing import Annotated
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field


async def save_patient_info(
    sex: Annotated[str, Field(description="sex of the patient")] = None,
    age: Annotated[int, Field(description="age of the patient")] = None,
    arrival_mode: Annotated[
        str | None, Field(description="Type of transportation to the hospital")
    ] = None,
    injury: Annotated[str | None, Field(description="Type of injury")] = None,
    symptom: Annotated[
        str | None, Field(description="The patient's main symptom or complaint")
    ] = None,
    symptoms_start: Annotated[
        str | None,
        Field(description="The start time of the patient's symptom or complaint"),
    ] = None,
    pain_intensity: Annotated[
        str | None,
        Field(description="The intensity of the pain from 1 to 10", le=10, ge=0),
    ] = None,
    additional_symptoms: Annotated[
        str | None, Field(description="Write any additional symptoms or complaints")
    ] = None,
    medication: Annotated[
        str | None, Field(description="Write any medications or treatments")
    ] = None,
    allergies: Annotated[str | None, Field(description="Write any allergies")] = None,
):
    from src.datasources.prisma import prisma
    print("save patiend info")
    try:
        # save to db
        db_patient = await prisma.patientrecord.upsert(
            where={"id": 1},
            data={
                "sex": sex,
                "age": age,
                "arrival_mode": arrival_mode,
                "injury": injury,
                "symptom": symptom,
                "symptoms_start": symptoms_start,
                "pain_intensity": pain_intensity,
                "additional_symptoms": additional_symptoms,
                "medication": medication,
                "allergies": allergies,
            },
            include={"id": True},
        )
    except Exception as e:
        raise ToolException(str(e))


save_patient_info_tool = StructuredTool.from_function(
    name="save_patient_info",
    description="use this to save patient information",
    coroutine=save_patient_info,
    handle_tool_error=True,
)