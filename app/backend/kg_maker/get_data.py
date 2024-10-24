from metapub import PubMedFetcher
from backend.abstract_retrieval.pubmed_retriever import PubMedAbstractRetriever
from backend.data_repository.local_storage import LocalJSONStore


# Query
query = "rad21 in breast cancer"

# Step 1: Use PubMedAbstractRetriever to get abstract data
pubmed_fetcher = PubMedFetcher()
abstract_retriever = PubMedAbstractRetriever(pubmed_fetcher)
abstracts = abstract_retriever.get_abstract_data(query)

# # Step 2: Use the retrieved data with LocalJSONStorage to persist them in local storage
storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)
query_id = store.save_dataset(abstracts, query)