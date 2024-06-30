import streamlit as st
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.base import Runnable
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate

class ChatAgent:
    def __init__(self, prompt: ChatPromptTemplate, llm: Runnable):
        """
        Initialize the ChatAgent.

        Args:
        - prompt (ChatPromptTemplate): The chat prompt template.
        - llm (Runnable): The language model runnable.
        """
        self.msgs = StreamlitChatMessageHistory(key="chat_history")
        self.llm = llm
        self.prompt = prompt
        self.chain = self.setup_chain()

    def setup_chain(self) -> RunnableWithMessageHistory:
        """
        Set up the chain for the ChatAgent.

        Returns:
        - RunnableWithMessageHistory: The configured chain with message history.
        """
        chain = self.prompt | self.llm
        return RunnableWithMessageHistory(
            chain,
            lambda session_id: self.msgs,
            input_messages_key="question",
            history_messages_key="history",
        )

    def display_messages(self):
        """
        Display messages in the chat interface.
        If no messages are present, adds a default AI message.
        """
        if len(self.msgs.messages) == 0:
            self.msgs.add_ai_message("How can I help you?")
        for msg in self.msgs.messages:
            st.chat_message(msg.type).write(msg.content)

    def start_conversation(self):
        """
        Start a conversation in the chat interface.
        Displays messages, prompts user for input, and handles AI response.
        """
        self.display_messages()
        user_question = st.chat_input(placeholder="Ask me anything!")
        if user_question:
            st.chat_message("human").write(user_question)
            config = {"configurable": {"session_id": "any"}}
            response = self.chain.invoke({"question": user_question}, config)
            st.chat_message("ai").write(response.content)