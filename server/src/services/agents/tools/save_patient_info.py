from typing import Annotated
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field
from prisma.types import PatientRecordCreateInput, PatientRecordUpdateInput


async def save_patient_info(
    user_id: Annotated[str, Field(description="user id")],
    sex: Annotated[str | None, Field(description="sex of the patient")] = None,
    age: Annotated[str | None, Field(description="age of the patient")] = None,
    arrival_mode: Annotated[
        str | None, Field(description="Type of transportation to the hospital")
    ] = None,
    injury: Annotated[str | None, Field(description="Type of injury")] = None,
    chief_complaint: Annotated[
        str | None, Field(description="The patient's main symptom or complaint")
    ] = None,
    mental_state: Annotated[
        str | None,
        Field(description="Description of the patient's mental state"),
    ] = None,
    pain_intensity: Annotated[
        str | None,
        Field(description="The intensity of the pain from 1 to 10", le=10, ge=0),
    ] = None,
    blood_pressure: Annotated[
        str | None, Field(description="Patients's blood pressure")
    ] = None,
    heart_rate: Annotated[str | None, Field(description="Patient's heart rate")] = None,
    respiratory_rate: Annotated[
        str | None, Field(description="Patient's respiratory rate")
    ] = None,
    body_temperature: Annotated[
        str | None, Field(description="Patient's body temperature")
    ] = None,
    oxygen_saturation: Annotated[
        str | None, Field(description="Patient's oxygen saturation")
    ] = None,
):
    from src.datasources.prisma import prisma

    input = {
        "sex": sex,
        "age": age,
        "arrivalMode": arrival_mode,
        "injury": injury,
        "chiefComplaint": chief_complaint,
        "mentalState": mental_state,
        "painIntensity": pain_intensity,
        "bloodPressure": blood_pressure,
        "heartRate": heart_rate,
        "respiratoryRate": respiratory_rate,
        "bodyTemperature": body_temperature,
        "oxygenSaturation": oxygen_saturation,
        "userId": user_id,
    }

    parsed_input = {}
    for key, value in input.items():
        if value is not None:
            parsed_input[key] = value

    try:
        db_patient = await prisma.patientrecord.find_first(where={"userId": user_id})

        if not db_patient:
            db_patient = await prisma.patientrecord.create(data=parsed_input)
        else:
            db_patient = await prisma.patientrecord.update(
                where={"id": db_patient.id}, data=parsed_input
            )
        return db_patient.model_dump_json()
    except Exception as e:
        raise ToolException(str(e))


save_patient_info_tool = StructuredTool.from_function(
    name="save_patient_info",
    description="use this to save patient information",
    coroutine=save_patient_info,
    handle_tool_error=True,
)
