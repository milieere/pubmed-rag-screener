import streamlit as st
from components.chat_utils import ChatAgent
from components.prompts import chat_prompt_template
from components.llm import llm

def main():
    st.set_page_config(
        page_title="Pubmed Abstract Screener",
        page_icon='💬',
        layout='wide'
    )

    # Define two columns with the same width
    col1, col2 = st.columns([1, 3])

    # In the first column, display an image
    with col1:
        st.image('../assets/pubmed-screener-logo.jpg')

    # In the second column, place text and interactive elements
    with col2:
        st.title("PubMed Screener")
        st.markdown("""
            PubMed Screener is a ChatGPT & PubMed powered insight generator from biomedical abstracts. 

            #### Example prompts 'describe what are you looking for'
            - "I'm interested in research on the use of CRISPR technology for enhancing gene therapy in neurodegenerative diseases."
            - "I want to find articles discussing the role of gut microbiota in modulating immune responses in autoimmune disorders."
            - "I need information on the development of novel drug delivery systems using nanotechnology for targeted cancer therapy."
            - "What is the current understanding of the genetic factors influencing susceptibility to infectious diseases in pediatric populations?"
        """)

    chat_agent = ChatAgent(prompt=chat_prompt_template, llm=llm)
    chat_agent.start_conversation()

if __name__ == "__main__":
    main()