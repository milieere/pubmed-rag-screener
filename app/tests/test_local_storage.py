import unittest
import os
import shutil
import tempfile
import json
from unittest.mock import patch, MagicMock
from backend.data_repository.models import UserQueryRecord, ScientificAbstract
from backend.data_repository.local_storage import LocalJSONStore


class TestLocalJSONStore(unittest.TestCase):
    def setUp(self):
        """Setup a temporary directory and initialize LocalJSONStore."""
        self.test_dir = tempfile.mkdtemp()
        self.store = LocalJSONStore(self.test_dir)

    def tearDown(self):
        """Clean up by removing the temporary directory after tests."""
        shutil.rmtree(self.test_dir)

    @patch('json.load')
    @patch('builtins.open')
    def test_read_dataset_success(self, mock_open, mock_json_load):
        """Test reading a dataset successfully."""
        query_id = 'test_query'
        expected_data = [{'doi': None, 'title': 'Sample Title', 'authors': None, 'year': None, 'abstract_content': 'Sample abstract'}]
        mock_json_load.return_value = expected_data

        result = self.store.read_dataset(query_id)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ScientificAbstract)
        self.assertEqual(result[0].abstract_content, 'Sample abstract')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_read_dataset_file_not_found(self, mock_open):
        """Test reading a dataset that does not exist."""
        with self.assertRaises(FileNotFoundError):
            self.store.read_dataset('nonexistent_query')

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_save_dataset(self, mock_open, mock_makedirs):
        """Test saving a dataset."""
        query_id = 'test_query'
        data_object = [ScientificAbstract(doi=None, title='Sample Title', authors=None, year=None, abstract_content='Sample abstract')]
        user_query_details = UserQueryRecord(user_query_id='query_1', user_query='Find data')

        self.store.save_dataset(query_id, data_object, user_query_details)
        self.assertTrue(mock_open.called)
        self.assertTrue(mock_makedirs.called)

    @patch('shutil.rmtree')
    def test_delete_dataset(self, mock_rmtree):
        """Test deleting a dataset."""
        query_id = 'test_query'
        os.makedirs(os.path.join(self.test_dir, query_id))
        self.store.delete_dataset(query_id)
        mock_rmtree.assert_called_once()

    def test_get_list_of_queries(self):
        query_id_1 = "test_query_1"
        user_query_id_1 = query_id_1  # Assuming user_query_id is the same as query_id
        user_query_1 = "Find data on plant growth"
        user_query_details_1 = UserQueryRecord(user_query_id=user_query_id_1, user_query=user_query_1)

        query_id_2 = "test_query_2"
        user_query_id_2 = query_id_2  # Assuming user_query_id is the same as query_id
        user_query_2 = "Find data on crop yield"
        user_query_details_2 = UserQueryRecord(user_query_id=user_query_id_2, user_query=user_query_2)

        self.store.save_dataset(query_id_1, [], user_query_details_1)
        self.store.save_dataset(query_id_2, [], user_query_details_2)

        query_list = self.store.get_list_of_queries()
        assert query_list[user_query_id_1] == user_query_1
        assert query_list[user_query_id_2] == user_query_2