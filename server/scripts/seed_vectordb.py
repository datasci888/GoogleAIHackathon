from src.configs.index import (
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    PINECONE_URL,
)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core.postprocessor import LLMRerank
from llama_index.llms.litellm import LiteLLM
llm = LiteLLM(model="gemini/gemini-pro",api_key=GOOGLE_API_KEY)

reranker = LLMRerank(llm)

def run():

    pc = Pinecone(api_key=PINECONE_API_KEY, host=PINECONE_URL)

    # uncoment this line if you want to create a new index
    # pc.create_index(
    #     name="core",
    #     dimension=1536,
    #     metric="euclidean",
    #     spec=ServerlessSpec(cloud="aws", region="us-west-2"),
    # )

    pinecone_index = pc.Index(host=PINECONE_URL)
    # try:
    #     pinecone_index.delete(delete_all=True, namespace="MTS")
    # except Exception as e:
    #     print(e)

    # # build docs
    documents = SimpleDirectoryReader(
        input_dir="./rag_documents", recursive=True
    ).load_data()

    llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
    node_parser = MarkdownElementNodeParser(llm=llm, num_workers=8)

    # build nodes
    nodes = node_parser.get_nodes_from_documents(documents)
    base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
    
    # build vector store and save
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="MTS")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # build index
    recursive_index = VectorStoreIndex(
        nodes=base_nodes + objects, storage_context=storage_context, show_progress=True
    )

    recursive_query_engine = recursive_index.as_query_engine(
        similarity_top_k=15,
        node_postprocessors=[reranker],
        verbose=True,
    )

    response = recursive_query_engine.query(
        "I have a light headache, which MTS classification would I fall into?"
    )
    print("response", response)
