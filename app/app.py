import streamlit as st
from metapub import PubMedFetcher
from components.chat_utils import ChatAgent
from components.chat_prompts import chat_prompt_template
from components.llm import llm
from components.layout_rendering import RenderDashboardHomepage
from components.chat_prompts import ChatPromptTemplate
from backend.abstract_retrieval.pubmed_retriever import PubMedAbstractRetriever
from backend.data_repository.local_storage import LocalJSONStore
from backend.rag_pipeline.chromadb_rag import ChromaDbRag
from backend.rag_pipeline.embeddings import embeddings


# Instantiate objects
pubmed_client = PubMedAbstractRetriever(PubMedFetcher())
data_repository = LocalJSONStore(storage_folder_path="backend/data")
rag_client = ChromaDbRag(persist_directory="backend/chromadb_storage", embeddings=embeddings)
chat_agent = ChatAgent(prompt=chat_prompt_template, llm=llm)
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

        # Some app info includign example questions
        homepage_layout.render_app_info()
        
        # Sector to formulate scientific question and fetch abstracts
        col_q, col_a = st.columns([1,1])

        with col_q:
            st.header("Enter your scientific question!")
            placeholder_text = "Type your scientific question here..."
            scientist_question = st.text_input("What is your question?", placeholder_text)
            get_articles = st.button('Get articles & Answer')

        with st.spinner('Fetching abstracts. This can take a while...'):
            if get_articles:
                if scientist_question and scientist_question != placeholder_text:

                    # Get abstracts data
                    retrieved_abstracts = pubmed_client.get_abstract_data(scientist_question)
                    if not retrieved_abstracts:
                        st.write('No abstracts found.')
                    else:
                        # Save abstarcts to storage and create vector index
                        query_id = data_repository.save_dataset(retrieved_abstracts, scientist_question)
                        documents = data_repository.create_document_list(retrieved_abstracts)
                        rag_client.create_vector_index_for_user_query(documents, query_id)
                        
                        # Display the answer to the user's initial question on the UI directly
                        chat_agent.get_answer_from_llm(scientist_question, documents).content

    # Beginning of the chatbot section
    st.header("Chat with the abstracts")

    # Display list of queries to select one to have a conversation about
    query_options = data_repository.get_list_of_queries()

    if query_options:
        selected_query = st.selectbox('Select a past query', options=list(query_options.values()), key='selected_query')
        
        if selected_query:
            selected_query_id = next(key for key, val in query_options.items() if val == selected_query)
            vector_index = rag_client.get_vector_index_by_user_query(selected_query_id)

            # Clear chat history when switching query to chat about
            if 'prev_selected_query' in st.session_state and st.session_state.prev_selected_query != selected_query:
                chat_agent.reset_history()

            st.session_state.prev_selected_query = selected_query
            chat_agent.start_conversation(vector_index, selected_query)


if __name__ == "__main__":
    main()