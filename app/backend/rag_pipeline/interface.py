from abc import ABC, abstractmethod
from langchain_core.documents.base import Document
from typing import Protocol, List
from langchain_core.embeddings import Embeddings
from langchain.vectorstores import VectorStore
    

class RagWorkflow(ABC):
    """ Interface for the rag workflow """
    
    @abstractmethod
    def create_vector_index_for_user_query(self, embeddings: Embeddings, documents: list, query_id: str) -> VectorStore:
        """ Create index based on documents retrieved for a specific user query """
        raise NotImplementedError
    
    @abstractmethod
    def get_vector_index_by_user_query_id(self, documents: List[Document], query_id: str, embeddings: Embeddings) -> VectorStore:
        """ 
        Create langchain VectorStore instance from list of langchain Documents 
        """
        raise NotImplementedError
    