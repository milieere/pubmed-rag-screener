from metapub import PubMedFetcher, PubMedArticle
from backend.data_repository.models import ScientificAbstract
from backend.abstract_retrieval.interface import DataRetriever
from typing import List

class PubMedDataRetriever(DataRetriever):
    def __init__(self, pubmed_fetch_object: PubMedFetcher):
        self.pubmed_fetch_object = pubmed_fetch_object

    def _get_abstract_list(self, query: str) -> List[str]:
        """ Fetch a list of PubMed IDs for the given query. """
        return self.pubmed_fetch_object.pmids_for_query(query)

    def _get_abstracts(self, pubmed_ids: List[str]) -> List[ScientificAbstract]:
        """ Fetch PubMed abstracts  """
        scientific_abstracts = []
        
        for id in pubmed_ids:
            abstract = self.pubmed_fetch_object.article_by_pmid(id)
            abstract_formatted = ScientificAbstract(
                doi=abstract.doi,
                title=abstract.title,
                author=abstract.authors,
                abstract_content=abstract.abstract
            )
            scientific_abstracts.append(abstract_formatted)
        
        return scientific_abstracts

    def get_abstract_data(self, scientist_question: str) -> List[ScientificAbstract]:
        """  Retrieve abstract data for a list of queries. """
        pmids = self._get_abstract_list(scientist_question)
        abstracts = self._get_abstracts(pmids)
        return abstracts