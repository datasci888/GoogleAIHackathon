import asyncio
from langchain_community.docstore.document import Document
from typing import Annotated
from langchain_core.tools import ToolException, StructuredTool
from pydantic import Field
from src.utils.knowledge_graph import KnowledgeGraph


def run(
    er_visit_id: Annotated[str, Field(description="erVisitId")],
    triplets: Annotated[
        list[str],
        Field(
            description="Triplets of patient informations to be saved",
            examples=[
                "Patient has a blurry eyes.",
                "Patient has a deep cough.",
                "Patient is 40 years old.",
            ],
        ),
    ],
):
    documents = []
    for triplet in triplets:
        documents.append(Document(page_content=triplet))

    try:

        kg = KnowledgeGraph(label=er_visit_id, verbose=True)
        knowledge = "\n".join(triplets)
        res = kg.store_knowledge(knowledge=knowledge)
        return f"""
```
{knowledge}
```
"""
    except Exception as e:
        raise ToolException(str(e))


tool = StructuredTool.from_function(
    name="save_patient_info",
    description="use this to save patient information",
    func=run,
    handle_tool_error=True,
)
