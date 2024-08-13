from typing import List
import chromadb
from langchain.vectorstores import VectorStore
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents.base import Document
from backend.rag_pipeline.interface import RagWorkflow
from config.logging_config import get_logger


class ChromaDbRag(RagWorkflow):
    """ 
    Simple RAG workflow with Chroma as vector store 
    """

    def __init__(self, persist_directory: str, embeddings: Embeddings):
        self.persist_directory = persist_directory
        self.embeddings = embeddings
        self.client = self._create_chromadb_client()
        self.logger = get_logger(__name__)
    
    def _create_chromadb_client(self):
        return chromadb.PersistentClient(path=self.persist_directory)
    
    def create_vector_index_for_user_query(self, documents: List[Document], query_id: str) -> VectorStore:
        """
        Create Chroma vector index and set query ID as collection name.
        """
        self.logger.info(f'Creating vector index for {query_id}')
        try:
            index = Chroma.from_documents(
                documents, 
                self.embeddings,
                client=self.client, 
                collection_name=query_id
            )
            return index
        except Exception as e:
            self.logger.error(f'There was an issue creating vector index for query: {query_id}. The issue: {e}')
            raise
    
    def get_vector_index_by_user_query(self, query_id: str) -> VectorStore:
        """
        Retrieve existing Chroma index by collection name set to query ID.
        """
        self.logger.info(f'Loading vector index for query: {query_id}')
        try:
            index = Chroma(
                client=self.client,
                collection_name=query_id,
                embedding_function=self.embeddings,
            )
            return index
        except Exception as e:
            self.logger.error(f'There was an issue retrieving vector index for query: {query_id}. The issue: {e}')
            raise

    