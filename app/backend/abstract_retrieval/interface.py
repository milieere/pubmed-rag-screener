from abc import ABC, abstractmethod
from typing import Protocol, List
from backend.data_repository.models import ScientificAbstract


class AbstractRetriever(Protocol):

    @abstractmethod
    def get_abstract_data(self, scientist_question: str) -> List[ScientificAbstract]:
        """ Retrieve a list of scientific abstracts based on a given query. """
        pass
