from neo4j_graphrag.experimental.components.entity_relation_extractor import (
    LLMEntityRelationExtractor,
    TextChunks, TextChunk, DocumentInfo
)
from neo4j_graphrag.experimental.components.resolver import SinglePropertyExactMatchResolver
import neo4j
import asyncio
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.llm.openai_llm import AzureOpenAILLM
from app.backend.kg_maker.neo4j.ontology import schema
from backend.data_repository.local_storage import LocalJSONStore
from backend.kg_maker.neo4j.kg_extraction_prompt import customized_prompt
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values(".env")

# Retrieve the abstracts from our local storage and read them as list of Langchain documents
storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)
documents = store.read_documents('query_6')

# Instantiate the extractor, set the lexical_graph property to True or False depending on requirements
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
    ),
    create_lexical_graph=False,
    prompt_template = customized_prompt
)

# Instantiate the Neo4J driver
driver = neo4j.GraphDatabase.driver(
    config["NEO4J_URI"], auth=(config["NEO4J_USERNAME"], config["NEO4J_PASSWORD"])
)

async def main():
    # Iterate over the documents, each document represents an abstract
    for doc in documents:
        # This will only have one chunk in it, since we do not split the abstracts to multiple chunks
        chunks=TextChunks(chunks=[TextChunk(text=f'ABSTRACT_TEXT: {doc.page_content}, ABSTRACT_METADATA: {str(doc.metadata)}', index=0, metadata=doc.metadata)])
        # Create the doc info from the metadata
        doc_info =  DocumentInfo(
            path=storage_folder_path,
            metadata={key: str(value) for key, value in doc.metadata.items()}
        )
        # Run extraction
        graph = await extractor.run(chunks=chunks, document_info=doc_info, schema=schema)
        # Write the results to Neo4J
        writer = Neo4jWriter(driver)
        await writer.run(graph)

    # Resolve properties
    resolver = SinglePropertyExactMatchResolver(driver, filter_query="WHERE not entity:Resolved")
    await resolver.run()

# Run the async code with asyncio
if __name__ == "__main__":
    asyncio.run(main())