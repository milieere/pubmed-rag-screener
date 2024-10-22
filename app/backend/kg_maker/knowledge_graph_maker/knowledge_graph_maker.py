from backend.data_repository.local_storage import LocalJSONStore
from knowledge_graph_maker.graph_maker import Ontology, GraphMaker
from knowledge_graph_maker import Neo4jGraphModel
from pydantic import BaseModel
from backend.kg_maker.knowledge_graph_maker.azureopenai_client import AzureOpenAIClient


storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)
documents = store.read_documents('query_6')

class Doc(BaseModel):
    text: str
    metadata: dict

docs = [Doc(text=document.page_content, metadata=document.metadata) for document in documents]

ontology = Ontology(
    labels=[
        {"Gene": "Gene name without any qualifiers"},
        {"Protein": "Protein encoded by a gene"},
        {"Disease": "Name of a disease or pathological condition"},
        {"Function": "Biological function or process associated with a gene or protein"},
        {"Pathology": "Observed pathological effects or symptoms"},
        {"Mutation": "Specific genetic mutation or variant"},
        {"Pathway": "Biological pathway involving the gene or protein"},
        {"CellType": "Specific cell type where the gene is expressed or relevant"},
        {"Experiment": "Experimental method or technique used in the study"},
        {"Drug": "Pharmaceutical compound or treatment"},
        {"Biomarker": "Biological marker associated with the gene or disease"},
    ],
    relationships=[
        "ENCODES",  # Gene ENCODES Protein
        "ASSOCIATED_WITH",  # Gene/Protein ASSOCIATED_WITH Disease
        "HAS_FUNCTION",  # Gene/Protein HAS_FUNCTION Function
        "CAUSES",  # Gene/Mutation CAUSES Pathology
        "PARTICIPATES_IN",  # Gene/Protein PARTICIPATES_IN Pathway
        "EXPRESSED_IN",  # Gene EXPRESSED_IN CellType
        "STUDIED_BY",  # Gene/Protein/Disease STUDIED_BY Experiment
        "INTERACTS_WITH",  # Protein INTERACTS_WITH Protein
        "REGULATES",  # Gene/Protein REGULATES Gene/Protein
        "TARGETS",  # Drug TARGETS Gene/Protein
        "INDICATES",  # Biomarker INDICATES Disease/Pathology
        "HAS_VARIANT",  # Gene HAS_VARIANT Mutation
    ]
)

llm_client = AzureOpenAIClient()
graph_maker = GraphMaker(ontology=ontology, llm_client=llm_client, verbose=False)
graph = graph_maker.from_documents(docs)

neo4j_graph = Neo4jGraphModel(edges=graph, create_indices=False)
neo4j_graph.save()
