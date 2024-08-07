import streamlit as st
from components.chat_utils import ChatAgent
from components.chat_prompts import chat_prompt_template
from components.llm import llm

def main():
    st.set_page_config(
        page_title="Pubmed Abstract Screener",
        page_icon='💬',
        layout='wide'
    )

    # Define two columns - this will make layout split horizontally
    col1, col2 = st.columns([1, 3])

    # Place the logo in the first column
    with col1:
        st.image('../assets/pubmed-screener-logo.jpg')

    # In the second column, place text explaining the purpose of the app and some example scientific questions that your user might ask.
    with col2:
        st.title("PubMed Screener")
        st.markdown("""
            PubMed Screener is a ChatGPT & PubMed powered insight generator from biomedical abstracts. 

            #### Example scientific questions
            - How can advanced imaging techniques and biomarkers be leveraged for early diagnosis and monitoring of disease progression in neurodegenerative disorders?
            - What are the potential applications of stem cell technology and regenerative medicine in the treatment of neurodegenerative diseases, and what are the associated challenges?
            - What are the roles of gut microbiota and the gut-brain axis in the pathogenesis of type 1 and type 2 diabetes, and how can these interactions be modulated for therapeutic benefit?
            - What are the molecular mechanisms underlying the development of resistance to targeted cancer therapies, and how can these resistance mechanisms be overcome?
        """)

    # This is the chatbot component
    chat_agent = ChatAgent(prompt=chat_prompt_template, llm=llm)
    chat_agent.start_conversation()

if __name__ == "__main__":
    main()