import json
import os
import time
import shutil
from typing import Dict, List
from backend.data_repository.models import UserQueryRecord, ScientificAbstract
from backend.data_repository.interface import UserQueryDataStore
from config.logging_config import get_logger


class LocalJSONStore(UserQueryDataStore):
    """ For local testing, to simulate database via local JSON files. """
    def __init__(self, storage_folder_path: str):
        self.storage_folder_path = storage_folder_path
        self.index_file_path = os.path.join(storage_folder_path, 'index.json')
        self.logger = get_logger(__name__)
        self.metadata_index = None

    def read_dataset(self, query_id: str) -> List[ScientificAbstract]:
        """ Read dataset containing abstracts from local storage. """
        try:
            with open(f'{self.storage_folder_path}/{query_id}/abstracts.json', 'r') as file:
                data = json.load(file)
                return [ScientificAbstract(**abstract_record) for abstract_record in data]
        except FileNotFoundError:
            self.logger.error(f'The JSON file for this query: {query_id} was not found.')
            raise FileNotFoundError('JSON file was not found.')

    def save_dataset(self, query_id: str, data_object: List[ScientificAbstract], user_query_details: UserQueryRecord) -> None:
        """ Save abstract dataset and query metadata to local storage and rebuild index. """
        try:
            os.makedirs(f'{self.storage_folder_path}/{query_id}', exist_ok=True)
            
            with open(f"{self.storage_folder_path}/{query_id}/abstracts.json", "w") as file:
                list_of_abstracts = [model.model_dump() for model in data_object]
                json.dump(list_of_abstracts, file, indent=4)

            with open(f"{self.storage_folder_path}/{query_id}/query_details.json", "w") as file:
                json_data = user_query_details.model_dump_json(indent=4)
                file.write(json_data)

            self.logger.info(f"Data for query ID {query_id} saved successfully.")
            self._rebuild_index()  # Rebuild index after saving new data

        except Exception as e:
            self.logger.error(f"Failed to save dataset for query ID {query_id}: {e}")
            raise RuntimeError(f"Failed to save dataset due to an error: {e}")
        
    def delete_dataset(self, query_id: str) -> None:
        """ Delete abstracts dataset and query metadata from local storage. """
        path_to_data = f'{self.storage_folder_path}/{query_id}'
        if os.path.exists(path_to_data):
            shutil.rmtree(path_to_data)
            self.logger.info(f"Directory '{path_to_data}' has been deleted.")
            self._rebuild_index()  # Rebuild index after deleting data
        else:
            self.logger.warning(f"Directory '{path_to_data}' does not exist and cannot be deleted.")

    def get_list_of_queries(self) -> Dict[str, str]:
        """ Get a dictionary containing query ID (as a key) and original user query (as a value) from the index. """
        return self.metadata_index

    def _rebuild_index(self) -> Dict[str, str]:
        """ Rebuild the index from all query details files. """
        index = {}
        query_data_paths = [os.path.join(self.storage_folder_path, name) for name in os.listdir(self.storage_folder_path)
                                    if os.path.isdir(os.path.join(self.storage_folder_path, name))]
        for query_data_path in query_data_paths:
            metadata_path = os.path.join(query_data_path, 'query_details.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as file:
                    metadata = json.load(file)
                    index[metadata['user_query_id']] = metadata['user_query']
            else:
                self.logger.warning(f"No query_details.json file found in {query_data_path}")
        with open(self.index_file_path, 'w') as file:
            json.dump(index, file, indent=4)
        self.metadata_index = index
        return index