from langchain_core.prompts import PromptTemplate
from components.llm import llm


def simplify_pubmed_query(scientist_question: str) -> str:
    """ Transform verbose queries to simplified queries for PubMed """
    prompt_formatted_str = pubmed_query_simplification_prompt.format(question=scientist_question)
    return llm.invoke(prompt_formatted_str).content

pubmed_query_simplification_prompt = PromptTemplate.from_template("""
    You are an expert in biomedical search queries. Your task is to simplify verbose and detailed user queries into concise and effective search queries suitable for the PubMed database. Focus on capturing the essential scientific or medical elements relevant to biomedical research.

    Here are examples of the queries that need simplification, and what the simplification should look like:

    Example 1:
    Verbose Query: Has there been any significant progress in Alzheimer's disease treatment using monoclonal antibodies in the last five years?
    Is simplification needed here: Yes.
    Simplified Query: Alzheimer's disease monoclonal antibodies treatment progress

    Example 2:
    Verbose Query: What are the latest findings on the impact of climate change on the incidence of vector-borne diseases in tropical regions?
    Is simplification needed here: Yes.
    Simplified Query: Climate change and vector-borne diseases in tropics

    Example 3:
    Verbose Query: Can you provide detailed insights into the recent advancements in gene therapy for treating hereditary blindness?
    Is simplification needed here: Yes.
    Simplified Query: Gene therapy for hereditary blindness advancements

    Example 4:
    Verbose Query: I am interested in understanding how CRISPR technology has been applied in the development of cancer therapies over the recent years.
    Is simplification needed here: Yes.
    Simplified Query: CRISPR technology in cancer therapy development

    Example 5:
    Verbose Query: Alzheimer's disease and amyloid plaques
    Is simplification needed here: No.
    Simplified Query: Alzheimer's disease and amyloid plaques

    Example 6:
    Verbose Query: Effects of aerobic exercise on elderly cognitive function
    Is simplification needed here: No.
    Simplified Query: Effects of aerobic exercise on elderly cognitive function

    Example 7:
    Verbose Query: Molecular mechanisms of insulin resistance in type 2 diabetes
    Is simplification needed here: No.
    Simplified Query: Molecular mechanisms of insulin resistance in type 2 diabetes

    Example 8:
    Verbose Query: Role of gut microbiota in human health and disease
    Is simplification needed here: No.
    Simplified Query: Role of gut microbiota in human health and disease

    This is the user query:
    {question}

    Only decide to simplify the user's question if it is verbose. If it is already simple enough, just return the original user question.
    Only output the simplified query, or the original query if it is simple enough already, nothing else!
""")

