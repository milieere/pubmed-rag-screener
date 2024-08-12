from abc import ABC, abstractmethod
from typing import List, Dict
from langchain_core.documents.base import Document
from backend.data_repository.models import UserQueryRecord, ScientificAbstract


class UserQueryDataStore(ABC):
    """Repository for interaction with abstract database"""

    @abstractmethod 
    def save_dataset(self, abstracts_data: List[ScientificAbstract], user_query_details: UserQueryRecord) -> None:
        """
        Save abstracts and details about the query to data storage.
        """
        raise NotImplementedError
    
    @abstractmethod 
    def read_dataset(self, query_id: str) -> List[ScientificAbstract]:
        """
        Retrieve abstracts for a given user query from data storage.
        """
        raise NotImplementedError
    
    @abstractmethod
    def delete_dataset(self, query_id: str) -> None:
        """
        Delete all data for a given query id from the database.
        """
        raise NotImplementedError

    @abstractmethod 
    def get_list_of_queries(self) -> Dict[str, str]:
        """
        Retrieve a dict with query id : user_query. Used to displayed list of queries on UI and for lookup. 
        """
        raise NotImplementedError
    
    def create_document_list(self, abstracts_data: List[ScientificAbstract]) -> List[Document]:
        return [
            Document(
                page_content=entry.abstract_content, metadata={
                    "source": entry.doi, "title": entry.title, 
                    "authors": entry.authors, "year_of_publication": entry.year
                }
            )
            for entry in abstracts_data
        ]
    
    def read_documents(self, query_id: str) -> List[Document]:
        """ Read the dataset and convert it to the required List[Document] """
        query_record = self.read_dataset(query_id)
        return self.create_document_list(query_record)