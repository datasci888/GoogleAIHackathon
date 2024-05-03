# The purpose is to create interface for storing and querying knowledge graph
# Each graph will be partitioned upon initialization
# Partition will be separated using a key string
from typing import List
from llama_index.core import Settings
from src.configs.index import (
    NEO4J_PASSWORD,
    NEO4J_URL,
    NEO4J_USERNAME,
    OPENAI_API_KEY,
)
from llama_index.core.indices import KnowledgeGraphIndex
import asyncio
from llama_index.core.schema import NodeWithScore
from llama_index.core import StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core.readers import StringIterableReader
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.graph_stores.types import GraphStore
from llama_index.core.storage import StorageContext
from llama_index.llms.openai import OpenAI


# define LLM
# llm = LiteLLM(model="gemini/gemini-pro", api_key=GOOGLE_API_KEY)
llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

Settings.llm = llm
Settings.chunk_size = 512


from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import KnowledgeGraphRAGRetriever


class KnowledgeGraph:
    def __init__(self, label: str, verbose: bool = False) -> None:
        self.label = label
        self.verbose = verbose
        self.graph_store = self._load_graph_store(label=self.label)
        self.storage_context = self._load_storage_context(graph_store=self.graph_store)
        self.index = self._load_index(storage_context=self.storage_context)

    def _load_graph_store(self, label: str) -> Neo4jGraphStore:
        graph_store = Neo4jGraphStore(
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            url=NEO4J_URL,
            database=NEO4J_USERNAME,
            node_label=label,
        )
        return graph_store

    def _load_storage_context(self, graph_store: GraphStore) -> StorageContext:
        storage_context = StorageContext.from_defaults(graph_store=graph_store)
        return storage_context

    def _load_index(self, storage_context: StorageContext) -> KnowledgeGraphIndex:
        index = KnowledgeGraphIndex(
            storage_context=storage_context, nodes=[], show_progress=self.verbose
        )
        return index

    def store_knowledge(self, knowledge: str) -> None:
        documents = StringIterableReader().load_data([knowledge])
        self.index = self.index.from_documents(
            documents=documents,
            storage_context=self.storage_context,
            include_embeddings=True,
            show_progress=self.verbose,
        )
        # self._close()

    # async def get_network_graph(self):
    #     network_graph = self.index.index_struct.table
    #     net = Network(notebook=True, cdn_resources="in_line", directed=True)
    #     net.from_nx(network_graph)
    #     net.show("example.html")
    #     await self._close()
    #     return network_graph

    def retrieve_knowledge(self, query: str) -> List[NodeWithScore]:
        index = KnowledgeGraphIndex(
            storage_context=self.storage_context, nodes=[], show_progress=self.verbose
        )
        response = index.as_retriever().retrieve(query)
        # self._close()
        return response

    def query_knowledge(self, query: str) -> RESPONSE_TYPE:
        graph_rag_retriever = KnowledgeGraphRAGRetriever(
            storage_context=self.storage_context, verbose=True, llm=llm
        )

        query_engine = RetrieverQueryEngine.from_args(
            graph_rag_retriever,
        )
        response = query_engine.query(query)

        # self._close()
        return response

    def _close(self) -> None:
        self.graph_store._driver.close()

    def delete_knowledge(self) -> None:
        self.graph_store.query(
            f"""
        MATCH (n:{self.label}) DETACH DELETE n
        """
        )
        # self._close()
