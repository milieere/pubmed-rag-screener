from knowledge_graph_maker.graph_maker import Ontology

ontology = Ontology(
    labels=[
        {"Gene": "Gene name without any qualifiers"},
        {"Protein": "Protein encoded by a gene"},
        {"Disease": "Name of a disease or pathological condition"},
        {"Function": "Biological function or process associated with a gene or protein"},
        {"Pathology": "Observed pathological effects or symptoms"},
        {"Mutation": "Specific genetic mutation or variant"},
        {"Pathway": "Biological pathway involving the gene or protein"},
        {"CellType": "Specific cell type where the gene is expressed or relevant"},
        {"Experiment": "Experimental method or technique used in the study"},
        {"Drug": "Pharmaceutical compound or treatment"},
        {"Biomarker": "Biological marker associated with the gene or disease"},
    ],
    relationships=[
        "ENCODES",  # Gene ENCODES Protein
        "ASSOCIATED_WITH",  # Gene/Protein ASSOCIATED_WITH Disease
        "HAS_FUNCTION",  # Gene/Protein HAS_FUNCTION Function
        "CAUSES",  # Gene/Mutation CAUSES Pathology
        "PARTICIPATES_IN",  # Gene/Protein PARTICIPATES_IN Pathway
        "EXPRESSED_IN",  # Gene EXPRESSED_IN CellType
        "STUDIED_BY",  # Gene/Protein/Disease STUDIED_BY Experiment
        "INTERACTS_WITH",  # Protein INTERACTS_WITH Protein
        "REGULATES",  # Gene/Protein REGULATES Gene/Protein
        "TARGETS",  # Drug TARGETS Gene/Protein
        "INDICATES",  # Biomarker INDICATES Disease/Pathology
        "HAS_VARIANT",  # Gene HAS_VARIANT Mutation
    ]
)
