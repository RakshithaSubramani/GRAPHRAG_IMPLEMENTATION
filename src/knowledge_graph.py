# src/knowledge_graph.py

from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core import Settings, SimpleDirectoryReader
from llama_index.core import KnowledgeGraphIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

# Configure Neo4j connection
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="neo4jgdb",  # change if your Neo4j password differs
    url="bolt://localhost:7687",
    database="neo4j"
)

# Use HuggingFace embeddings instead of OpenAI
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.chunk_size = 512
Settings.llm = None   # 🚨 disable default OpenAI LLM

def build_knowledge_graph(data_path="data"):
    """
    Build and return a KnowledgeGraphIndex and its storage context.
    """
    # Load documents
    documents = SimpleDirectoryReader(data_path).load_data()

    # Create a Knowledge Graph Index (no OpenAI, only HuggingFace embeddings)
    index = KnowledgeGraphIndex.from_documents(
        documents,
        max_triplets_per_chunk=10,
        graph_store=graph_store,
        embed_model=Settings.embed_model,
        llm=None,                  # 🚨 explicitly disable OpenAI LLM
        show_progress=True
    )

    # Return index + storage context
    return index, index.storage_context

if __name__ == "__main__":
    index, storage_context = build_knowledge_graph()
    print("✅ Knowledge graph built and stored in Neo4j.")
