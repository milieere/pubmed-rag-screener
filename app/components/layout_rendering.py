import streamlit as st
from backend.data_repository.interface import UserQueryDataStore

class RenderDashboardHomepage():

    def render_app_info(self):
        st.title("PubMed Screener")
        st.markdown("""
            PubMed Screener is a ChatGPT & PubMed powered insight generator from biomedical abstracts.
        """)

        # Adding custom HTML and CSS for an improved hover-over tooltip
        st.markdown("""
            <style>
            .tooltip {
                position: relative;
                display: inline-block;
                border-bottom: 1px dotted black; /* Style for the hoverable text */
            }

            .tooltip .tooltiptext {
                visibility: hidden;
                width: 800px; /* Width to fit content */
                background-color: #f9f9f9;
                color: #000;
                text-align: left;
                border-radius: 6px;
                padding: 15px;
                position: absolute;
                z-index: 1;
                bottom: 100;
                right: -430px; /* Positioning to the right and slightly offset */
                opacity: 0;
                transition: opacity 0.5s;
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.8); /* Adding some shadow for better visibility */
            }

            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            </style>
            <div class="tooltip">🔍 Example Questions
                <span class="tooltiptext">
                    <strong>Example scientific questions:</strong>
                    <ul>
                        <li>How can advanced imaging techniques and biomarkers be leveraged for early diagnosis and monitoring of disease progression in neurodegenerative disorders?</li>
                        <li>What are the potential applications of stem cell technology and regenerative medicine in the treatment of neurodegenerative diseases, and what are the associated challenges?</li>
                        <li>What are the roles of gut microbiota and the gut-brain axis in the pathogenesis of type 1 and type 2 diabetes, and how can these interactions be modulated for therapeutic benefit?</li>
                        <li>What are the molecular mechanisms underlying the development of resistance to targeted cancer therapies, and how can these resistance mechanisms be overcome?</li>
                    </ul>
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.text("")
