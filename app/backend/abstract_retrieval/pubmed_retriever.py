from typing import List
from metapub import PubMedFetcher
from backend.data_repository.models import ScientificAbstract
from backend.abstract_retrieval.interface import AbstractRetriever
from config.logging_config import get_logger


class PubMedAbstractRetriever(AbstractRetriever):
    def __init__(self, pubmed_fetch_object: PubMedFetcher):
        self.pubmed_fetch_object = pubmed_fetch_object
        self.logger = get_logger(__name__)

    def _get_abstract_list(self, query: str) -> List[str]:
        """ Fetch a list of PubMed IDs for the given query. """
        self.logger.info(f'Searching abstracts for query: {query}')
        return self.pubmed_fetch_object.pmids_for_query(query)

    def _get_abstracts(self, pubmed_ids: List[str]) -> List[ScientificAbstract]:
        """ Fetch PubMed abstracts  """
        self.logger.info(f'Fetching abstract data for following pubmed_ids: {pubmed_ids}')
        scientific_abstracts = []
        
        for id in pubmed_ids:
            abstract = self.pubmed_fetch_object.article_by_pmid(id)
            if abstract.abstract is None:
                continue
            abstract_formatted = ScientificAbstract(
                doi=abstract.doi,
                title=abstract.title,
                authors=', '.join(abstract.authors),
                year=abstract.year,
                abstract_content=abstract.abstract
            )
            scientific_abstracts.append(abstract_formatted)

        self.logger.info(f'Total of {len(scientific_abstracts)} abstracts retrieved.')
        
        return scientific_abstracts

    def get_abstract_data(self, scientist_question: str) -> List[ScientificAbstract]:
        """  Retrieve abstract list for scientist query. """
        pmids = self._get_abstract_list(scientist_question)
        abstracts = self._get_abstracts(pmids)
        return abstracts
