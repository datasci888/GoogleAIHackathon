from pinecone import Pinecone
from src.configs.index import GOOGLE_API_KEY, PINECONE_API_KEY, PINECONE_URL
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.postprocessor import LLMRerank
from llama_index.llms.litellm import LiteLLM


async def aquery(query: str):
    pc = Pinecone(api_key=PINECONE_API_KEY)

    pinecone_index = pc.Index(host=PINECONE_URL)

    llm = LiteLLM(model="gemini/gemini-pro", api_key=GOOGLE_API_KEY)

    reranker = LLMRerank(llm)

    vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="MTS")

    recursive_index = VectorStoreIndex.from_vector_store(vector_store)

    recursive_query_engine = recursive_index.as_query_engine(
        similarity_top_k=10,
        node_postprocessors=[reranker],
        verbose=True
    )

    response = await recursive_query_engine.aquery(
        str_or_query_bundle=f"""Let's think step by step.
        List all presentational complaints related to these symptoms
        
        {query}
        """
    )

    return response.response


# import asyncio

# asyncio.run(aquery(query="my tummy hurt"))
