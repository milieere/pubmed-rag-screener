from typing import List
import streamlit as st
from langchain_core.documents.base import Document
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.base import Runnable
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores import VectorStore


class ChatAgent:
    def __init__(self, prompt: ChatPromptTemplate, llm: Runnable):
        """
        Initialize the ChatAgent.

        Args:
        - prompt (ChatPromptTemplate): The chat prompt template.
        - llm (Runnable): The language model runnable.
        """
        self.history = StreamlitChatMessageHistory(key="chat_history")
        self.llm = llm
        self.prompt = prompt
        self.chain = self.setup_chain()
    
    def reset_history(self) -> None:
        self.history.clear()

    def setup_chain(self) -> RunnableWithMessageHistory:
        """
        Set up the chain for the ChatAgent.

        Returns:
        - RunnableWithMessageHistory: The configured chain with message history.
        """
        chain = self.prompt | self.llm
        return RunnableWithMessageHistory(
            chain,
            lambda session_id: self.history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def display_messages(self):
        """
        Display messages in the chat interface.
        If no messages are present, adds a default AI message.
        """
        if len(self.history.messages) == 0:
            self.history.add_ai_message("How can I help you?")
        for msg in self.history.messages:
            st.chat_message(msg.type).write(msg.content)
    
    def format_retreieved_abstracts_for_prompt(self, documents: List[Document], cut_off: int = 5) -> str:
        """
        Format retrieved documents in a string to be passed to LLM.
        """
        formatted_strings = []
        for doc in documents[:cut_off]:
            formatted_str = f"ABSTRACT TITLE: {doc.metadata['title']}, ABSTRACT CONTENT: {doc.page_content}, ABSTRACT DOI: {doc.metadata['source']}"
            formatted_strings.append(formatted_str)
        return "; ".join(formatted_strings)

    def start_conversation(self, retriever: VectorStore):
        """
        Start a conversation in the chat interface.
        Displays messages, prompts user for input, and handles AI response.
        """
        self.display_messages()
        user_question = st.chat_input(placeholder="Ask me anything!")
        if user_question:
            documents = retriever.similarity_search(user_question)
            retrieved_abstracts = self.format_retreieved_abstracts_for_prompt(documents)
            st.chat_message("human").write(user_question)
            config = {"configurable": {"session_id": "any"}}
            response = self.chain.invoke(
                {
                    "question": user_question, 
                    "retrieved_abstracts": retrieved_abstracts,
                    "chat_history": self.history.messages[:3]
                }, config
            )
            st.chat_message("ai").write(response.content)