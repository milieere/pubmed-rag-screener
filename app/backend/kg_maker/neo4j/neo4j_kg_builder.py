from neo4j_graphrag.experimental.components.entity_relation_extractor import (
    LLMEntityRelationExtractor,
    TextChunks, TextChunk, DocumentInfo
)
from neo4j_graphrag.experimental.components.resolver import (
    SinglePropertyExactMatchResolver,
)
import neo4j
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.experimental.components.types import Neo4jGraph
from neo4j_graphrag.llm.openai_llm import AzureOpenAILLM
from dotenv import dotenv_values
from backend.kg_maker.neo4j.neo4j_ontology import schema
from backend.data_repository.local_storage import LocalJSONStore


config = dotenv_values(".env")

extractor = LLMEntityRelationExtractor(
    llm=AzureOpenAILLM(
        model_name=config['AZURE_OPENAI_DEPLOYMENT_NAME'],
        model_params={
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        azure_endpoint=config['AZURE_ENDPOINT'],
        api_key=config['AZURE_OPENAI_API_KEY'],
        azure_deployment=config['AZURE_OPENAI_DEPLOYMENT_NAME'],
        api_version=config['API_VERSION_LLM'],
    )
)

storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)
documents = store.read_documents('query_6')

driver = neo4j.GraphDatabase.driver(
    config["NEO4J_URI"], auth=(config["NEO4J_USERNAME"], config["NEO4J_PASSWORD"])
)

async def main():
    for doc in documents:
        chunks=TextChunks(chunks=[TextChunk(text=doc.page_content, index=0, metadata=doc.metadata)])
        doc_info =  DocumentInfo(
            path=storage_folder_path,
            metadata={key: str(value) for key, value in doc.metadata.items()}
        )
        graph = await extractor.run(chunks=chunks, document_info=doc_info, schema=schema)
        writer = Neo4jWriter(driver)
        await writer.run(graph)

    resolver = SinglePropertyExactMatchResolver(driver, filter_query="WHERE not entity:Resolved")
    await resolver.run()

import asyncio
if __name__ == "__main__":
    asyncio.run(main())