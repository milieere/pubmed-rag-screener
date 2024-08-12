from typing import List
from backend.data_repository.local_storage import LocalJSONStore
from backend.data_repository.models import UserQueryRecord, ScientificAbstract

# Create an instance of LocalJSONStore
storage_folder_path = "backend/data"
store = LocalJSONStore(storage_folder_path)

# Define a sample user query
query_id = "query_1"
user_query_id = "user_query_1"
user_query = "Find data on plant growth"
user_query_details = UserQueryRecord(user_query_id=user_query_id, user_query=user_query)

# Create some sample scientific abstracts
abstract_1 = ScientificAbstract(
    doi="10.1111/j.1365-3040.2009.02041.x",
    title="Plant growth and development under drought stress: physiological responses and adaptive strategies",
    authors=["Farooq, M.", "Wahid, A.", "Kobayashi, N.", "Fujita, D.", "Basra, S.M.A."],
    year=2009,
    abstract_content="Drought stress is a major abiotic stress that limits plant growth and productivity worldwide..."
)

abstract_2 = ScientificAbstract(
    doi="10.1007/s11104-011-0805-8",
    title="Root traits contributing to plant productivity under drought conditions",
    authors=["Comas, L.H.", "Becker, S.R.", "Cruz, V.M.V.", "Byrne, P.F.", "Dierig, D.A."],
    year=2013,
    abstract_content="Drought is one of the most important environmental stresses limiting plant productivity..."
)

abstracts = [abstract_1, abstract_2]

# Save the dataset and user query details
store.save_dataset(query_id, abstracts, user_query_details)

# Get the list of queries
query_list = store.get_list_of_queries()
print("List of queries:")
for user_query_id, user_query in query_list.items():
    print(f"User Query ID: {user_query_id}, User Query: {user_query}")

# Load the dataset for the query
loaded_dataset: List[ScientificAbstract] = store.read_dataset(query_id)
print("\nLoaded dataset:")
for abstract in loaded_dataset:
    print(f"Title: {abstract.title}")
    print(f"Authors: {', '.join(abstract.authors)}")
    print(f"Abstract: {abstract.abstract_content}")
    print()


print(store.metadata_index)
# Delete the dataset
# store.delete_dataset(query_id)