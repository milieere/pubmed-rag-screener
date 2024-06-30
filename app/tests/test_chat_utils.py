import unittest
from unittest.mock import patch, MagicMock, call
from components.chat_utils import ChatAgent

class TestChatAgent(unittest.TestCase):
    def setUp(self):
        self.prompt_mock = MagicMock()
        self.llm_mock = MagicMock()
        self.chat_agent = ChatAgent(self.prompt_mock, self.llm_mock)

    @patch('streamlit.chat_input', return_value="Test question")
    @patch('streamlit.chat_message')
    def test_start_conversation(self, mock_chat_message, mock_chat_input):
        self.chat_agent.start_conversation()
        mock_chat_message.assert_called_with("ai")

    def test_setup_chain(self):
        self.chat_agent.setup_chain()
        self.assertIsNotNone(self.chat_agent.chain)

    @patch('streamlit.chat_message')
    def test_display_messages(self, mock_chat_message):
        self.chat_agent.display_messages()
        mock_chat_message.assert_called() 

    @patch('streamlit.chat_input', return_value="tes test")
    @patch('streamlit.chat_message')
    def test_start_conversation_user_question(self, mock_chat_message, mock_chat_input):
        self.chat_agent.start_conversation()
        mock_chat_message.assert_has_calls([call('human').write('tes test')])
    
    @patch('streamlit.chat_input', return_value=None)
    @patch('streamlit.chat_message')
    def test_start_conversation_user_question(self, mock_chat_message, mock_chat_input):
        self.chat_agent.start_conversation()
        mock_chat_message.assert_has_calls([call('ai').write('How can I help you?')])


if __name__ == '__main__':
    unittest.main()