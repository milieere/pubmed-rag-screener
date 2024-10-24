from neo4j_graphrag.experimental.components.schema import (
    SchemaBuilder,
    SchemaEntity,
    SchemaProperty,
    SchemaRelation,
)

schema_builder = SchemaBuilder()

schema = schema_builder.create_schema_model(
    entities=[
        SchemaEntity(
            label="Gene",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Protein",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Disease",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Function",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Pathology",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Mutation",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Pathway",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="CellType",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Experiment",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Drug",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
        SchemaEntity(
            label="Biomarker",
            properties=[
                SchemaProperty(name="name", type="STRING"),
                SchemaProperty(name="description", type="STRING"),
            ],
        ),
    ],
    relations=[
        SchemaRelation(label="ENCODES"),
        SchemaRelation(label="ASSOCIATED_WITH"),
        SchemaRelation(label="HAS_FUNCTION"),
        SchemaRelation(label="CAUSES"),
        SchemaRelation(label="PARTICIPATES_IN"),
        SchemaRelation(label="EXPRESSED_IN"),
        SchemaRelation(label="STUDIED_BY"),
        SchemaRelation(label="INTERACTS_WITH"),
        SchemaRelation(label="REGULATES"),
        SchemaRelation(label="TARGETS"),
        SchemaRelation(label="INDICATES"),
        SchemaRelation(label="HAS_VARIANT"),
    ],
    potential_schema=[
        ("Gene", "ENCODES", "Protein"),
        ("Gene", "ASSOCIATED_WITH", "Disease"),
        ("Protein", "ASSOCIATED_WITH", "Disease"),
        ("Gene", "HAS_FUNCTION", "Function"),
        ("Protein", "HAS_FUNCTION", "Function"),
        ("Gene", "CAUSES", "Pathology"),
        ("Mutation", "CAUSES", "Pathology"),
        ("Gene", "PARTICIPATES_IN", "Pathway"),
        ("Protein", "PARTICIPATES_IN", "Pathway"),
        ("Gene", "EXPRESSED_IN", "CellType"),
        ("Gene", "STUDIED_BY", "Experiment"),
        ("Protein", "STUDIED_BY", "Experiment"),
        ("Disease", "STUDIED_BY", "Experiment"),
        ("Protein", "INTERACTS_WITH", "Protein"),
        ("Gene", "REGULATES", "Gene"),
        ("Gene", "REGULATES", "Protein"),
        ("Protein", "REGULATES", "Gene"),
        ("Protein", "REGULATES", "Protein"),
        ("Drug", "TARGETS", "Gene"),
        ("Drug", "TARGETS", "Protein"),
        ("Biomarker", "INDICATES", "Disease"),
        ("Biomarker", "INDICATES", "Pathology"),
        ("Gene", "HAS_VARIANT", "Mutation"),
    ],
)