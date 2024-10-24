from backend.data_repository.local_storage import LocalJSONStore
from knowledge_graph_maker.graph_maker import GraphMaker
from knowledge_graph_maker import Neo4jGraphModel
from pydantic import BaseModel
from backend.kg_maker.knowledge_graph_maker.azureopenai_client import AzureOpenAIClient
from backend.kg_maker.knowledge_graph_maker.ontology import ontology


# Retrieve abstracts data from the local storage
storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)
documents = store.read_documents('query_6')

# Define the document model expected by the library
class Doc(BaseModel):
    text: str
    metadata: dict

# Transform the langchain document format to the model expeczed by the library
docs = [Doc(text=document.page_content, metadata=document.metadata) for document in documents]

# Instantiate the LLM client
llm_client = AzureOpenAIClient()
# Instantiate the GraphMaker class and pass the ontology and LLM client
graph_maker = GraphMaker(ontology=ontology, llm_client=llm_client, verbose=False)
#Run the extraction
graph = graph_maker.from_documents(docs)

# Load the extracted graph to Neo4J
neo4j_graph = Neo4jGraphModel(edges=graph, create_indices=False)
neo4j_graph.save()
