from pydantic import BaseModel
from llama_index.core.program import LLMTextCompletionProgram
from src.configs.index import GOOGLE_API_KEY
from llama_index.llms.litellm import LiteLLM

async def astructured_text_extraction(text: str, output:BaseModel)-> BaseModel:
    """
    Asynchronously extracts all information in the provided text using Gemini LLM.
    
    Args:
        text (str): The text from which information needs to be extracted.
        output (BaseModel): The output model type for the extracted information.
    
    Returns:
        BaseModel: The extracted information based on the provided text.
    """
    prompt_template_str = f"""\
        Extract all information in the text bellow. \
        {text}.\
    """
    
    llm = LiteLLM(model="gemini/gemini-pro",api_key=GOOGLE_API_KEY)
    program = LLMTextCompletionProgram.from_defaults(
        output_cls=output,
        prompt_template_str=prompt_template_str,
        verbose=True,
        llm=llm
    )
    
    res = await program.acall()
    
    return res

import asyncio

class Name(BaseModel):
    """Name to extract"""
    name:str
res :Name= asyncio.run(astructured_text_extraction(output=Name,text="hello my name is viky"))

print("res",res)