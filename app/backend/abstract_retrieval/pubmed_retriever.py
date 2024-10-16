from typing import List
import time
import random
from metapub import PubMedFetcher
from backend.data_repository.models import ScientificAbstract
from backend.abstract_retrieval.interface import AbstractRetriever
from backend.abstract_retrieval.pubmed_query_simplification import simplify_pubmed_query
from config.logging_config import get_logger


class PubMedAbstractRetriever(AbstractRetriever):
    def __init__(self, pubmed_fetch_object: PubMedFetcher):
        self.pubmed_fetch_object = pubmed_fetch_object
        self.logger = get_logger(__name__)

    def _simplify_pubmed_query(self, query: str, simplification_function: callable = simplify_pubmed_query) -> str:
        return simplification_function(query)

    def _get_abstract_list(self, query: str, simplify_query: bool = True) -> List[str]:
        """ Fetch a list of PubMed IDs for the given query. """
        if simplify_query:
            self.logger.info(f'Trying to simplify scientist query {query}')
            query_simplified = self._simplify_pubmed_query(query)

            if query_simplified != query:
                self.logger.info(f'Initial query simplified to: {query_simplified}')
                query = query_simplified
            else:
                self.logger.info('Initial query is simple enough and does not need simplification.')

        self.logger.info(f'Searching abstracts for query: {query}')
        return self.pubmed_fetch_object.pmids_for_query(query)
    
    def _get_abstracts(self, pubmed_ids: List[str]) -> List[ScientificAbstract]:
        """ Fetch PubMed abstracts """
        self.logger.info(f'Fetching abstract data for following pubmed_ids: {pubmed_ids}')
        scientific_abstracts = []

        for id in pubmed_ids:
            initial_delay = 1  # Initial delay in seconds
            max_attempts = 10
            success = False

            for attempt in range(max_attempts):
                try:
                    abstract = self.pubmed_fetch_object.article_by_pmid(id)
                    if abstract.abstract is None:
                        break
                    abstract_formatted = ScientificAbstract(
                        doi=abstract.doi,
                        title=abstract.title,
                        authors=', '.join(abstract.authors),
                        year=abstract.year,
                        abstract_content=abstract.abstract
                    )
                    scientific_abstracts.append(abstract_formatted)
                    success = True
                    break
                except Exception as e:
                    wait_time = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                    self.logger.warning(f'Retry {attempt + 1} for ID {id} failed. Error: {e}. Retrying in {wait_time:.2f} seconds.')
                    time.sleep(wait_time)
            
            if not success:
                self.logger.error(f'Failed to retrieve the abstract with ID: {id} after {max_attempts} attempts.')
        self.logger.info(f'Total of {len(scientific_abstracts)} abstracts retrieved.')
        return scientific_abstracts

    def get_abstract_data(self, scientist_question: str, simplify_query: bool = True) -> List[ScientificAbstract]:
        """  Retrieve abstract list for scientist query. """
        pmids = self._get_abstract_list(scientist_question, simplify_query)
        abstracts = self._get_abstracts(pmids)
        return abstracts
