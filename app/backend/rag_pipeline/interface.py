from typing import List
from abc import ABC, abstractmethod
from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings
from langchain.vectorstores import VectorStore
    

class RagWorkflow(ABC):
    """ 
    Interface for the rag workflow 
    """

    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
    
    @abstractmethod
    def create_vector_index_for_user_query(self, documents: List[Document], query_id: str) -> VectorStore:
        """ 
        Create vector index based on documents retrieved for a specific user query 
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_vector_index_by_user_query(self, documents: List[Document], query_id: str) -> VectorStore:
        """ 
        Get existing vector index from a query ID
        """
        raise NotImplementedError
    