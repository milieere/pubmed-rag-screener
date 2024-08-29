import streamlit as st
from components.chat_utils import ChatAgent
from components.chat_prompts import chat_prompt_template
from components.llm import llm
from components.layout_rendering import RenderDashboardHomepage
from backend.data_repository.local_storage import LocalJSONStore
from backend.rag_pipeline.chromadb_rag import ChromaDbRag
from backend.rag_pipeline.embeddings import embeddings


data_repository = LocalJSONStore(storage_folder_path="backend/data")
rag_client = ChromaDbRag(persist_directory="backend/chromadb_storage", embeddings=embeddings)
homepage_layout = RenderDashboardHomepage()

def main():
    st.set_page_config(
        page_title="Pubmed Abstract Screener",
        page_icon='💬',
        layout='wide'
    )

    # Define two columns - this will make layout split horizontally
    column_logo, column_app_info = st.columns([1, 4])

    # Place the logo in the first column
    with column_logo:
        st.image('../assets/pubmed-screener-logo.jpg')

    # In the second column, place text explaining the purpose of the app and some example scientific questions that your user might ask.
    with column_app_info:
        homepage_layout.render_column_with_app_info()
        placeholder_text = "Type your scientific question here..."
        title = st.text_input("What is your question?", placeholder_text)

    # This is the chatbot component
    
    tab_chatbot, tab2 = st.tabs(["Chat with Abstracts", "Explore abstracts"])

    with tab_chatbot:
        st.header("Chat with the abstracts")
        chat_agent = ChatAgent(prompt=chat_prompt_template, llm=llm)
        chat_agent.start_conversation()

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
        
if __name__ == "__main__":
    main()