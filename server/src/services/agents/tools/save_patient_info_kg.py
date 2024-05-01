from langchain_community.docstore.document import Document
from typing import Annotated
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field


async def arun(
    er_visit_id: Annotated[str, Field(description="erVisitId")],
    triplets: Annotated[
        list[str],
        Field(
            description="Triplets of patient informations to be saved",
            examples=[
                "Patient has a fever",
                "Patient has a cough",
                "Patient has a shortness of breath",
            ],
        ),
    ]
):
    documents = []
    for triplet in triplets:
        documents.append(Document(page_content=triplet))

    try:
        from src.utils.knowledge_graph import KnowledgeGraph

        kg = KnowledgeGraph(label=er_visit_id, verbose=True)
        knowledge = "\n".join(triplets)
        res = await kg.astore_knowledge(knowledge=knowledge)
        return f"{knowledge} has been saved" 
    except Exception as e:
        raise ToolException(str(e))


tool = StructuredTool.from_function(
    name="save_patient_info",
    description="use this to save patient information",
    coroutine=arun,
    handle_tool_error=True,
)
