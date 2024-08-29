import streamlit as st
from metapub import PubMedFetcher
from components.chat_utils import ChatAgent
from components.chat_prompts import chat_prompt_template
from components.llm import llm
from components.layout_rendering import RenderDashboardHomepage
from backend.abstract_retrieval.pubmed_retriever import PubMedAbstractRetriever
from backend.data_repository.local_storage import LocalJSONStore
from backend.rag_pipeline.chromadb_rag import ChromaDbRag
from backend.rag_pipeline.embeddings import embeddings


# Instantiate objects
pubmed_client = PubMedAbstractRetriever(PubMedFetcher())
data_repository = LocalJSONStore(storage_folder_path="backend/data")
rag_client = ChromaDbRag(persist_directory="backend/chromadb_storage", embeddings=embeddings)
homepage_layout = RenderDashboardHomepage()

data_repository.create_document_list(data_repository.read_dataset('query_5'))

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
        homepage_layout.render_app_info()

        st.header("Enter your scientific question!")
        placeholder_text = "Type your scientific question here..."
        scientist_question = st.text_input("What is your question?", placeholder_text)

        with st.spinner('Fetching abstracts. This can take a while...'):
            if st.button('Get articles'):
                if scientist_question and scientist_question != placeholder_text:
                    retrieved_abstracts = pubmed_client.get_abstract_data(scientist_question)
                    if not retrieved_abstracts:
                        st.write('No abstracts found.')
                    else:
                        query_id = data_repository.save_dataset(retrieved_abstracts, scientist_question)
                        documents = data_repository.create_document_list(retrieved_abstracts)
                        rag_client.create_vector_index_for_user_query(documents, query_id)

    # This is the chatbot component
    st.header("Chat with the abstracts")
    homepage_layout.render_last_queries(data_repository)
    chat_agent = ChatAgent(prompt=chat_prompt_template, llm=llm)
    chat_agent.start_conversation()

if __name__ == "__main__":
    main()