from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents.base import Document
from backend.data_repository.models import UserQueryRecord

class UserQueryDataStore(ABC):
    """Repository for interaction with abstract database"""

    @abstractmethod 
    def save_dataset(self, data_object: UserQueryRecord) -> None:
        """
        Save dataset to data storage.
        """
        raise NotImplementedError
    
    @abstractmethod 
    def read_dataset(self, user_query: str) -> UserQueryRecord:
        """
        Retrieve dataset for a particular user query from data storage.
        """
        raise NotImplementedError

    @abstractmethod 
    def get_list_of_queries(self) -> List[str]:
        """
        Retrieve a list of queries to be displayed on the UI. 
        """
        raise NotImplementedError
    
    def create_document_list(self, query_record: UserQueryRecord) -> List[Document]:
        return [
            Document(
                page_content=entry.abstract_content, metadata={
                    "source": entry.doi, "title": entry.title, 
                    "authors": entry.authors, "year_of_publication": entry.year
                }
            )
            for entry in query_record.abstracts
        ]
    
    def read_documents(self, query_id: str) -> List[Document]:
        """ Read the dataset and convert it to the required List[Document] """
        query_record = self.read_dataset(query_id)
        return self.create_document_list(query_record)