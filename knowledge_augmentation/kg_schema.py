"""
Knowledge Graph Schema Definition for Biomedical Research Papers

This module defines a comprehensive schema for the biomedical knowledge graph,
including entity types and relationship types specifically designed for PubMed XML
article processing. The schema is structured to support the Knowledge Augmented
Generation (KAG) pattern used in the Nexus Scholar AI system.

Schema Structure:
1. Entity Types: Defines categories of biomedical entities (e.g., DRUG, DISEASE, GENE)
   with descriptions and examples to guide entity extraction.

2. Relation Types: Defines valid relationships between entities (e.g., TREATS, CAUSES)
   with descriptions, valid subject/object entity type constraints, and examples.

3. Utility Functions: Provides functions to validate and query the schema, enabling
   the knowledge graph builder to ensure data consistency.

This schema is used by the entity extraction and relation extraction components
to identify and categorize biomedical entities and relationships from the text.
It also supports mutual indexing between the knowledge graph and source text
for accurate citation generation.
"""

# Define entity types for the biomedical knowledge graph
ENTITY_TYPES = {
    "DRUG": {
        "description": "Medications, therapeutic compounds, and chemical substances used for treatment",
        "examples": ["aspirin", "metformin", "atorvastatin"]
    },
    "DISEASE": {
        "description": "Medical conditions, disorders, syndromes, and pathologies",
        "examples": ["diabetes", "COVID-19", "hypertension"]
    },
    "GENE": {
        "description": "Genes, gene products, and genetic markers",
        "examples": ["BRCA1", "TP53", "APOE"]
    },
    "PROTEIN": {
        "description": "Proteins, enzymes, and protein complexes",
        "examples": ["ACE2", "cytochrome P450", "insulin receptor"]
    },
    "PATHWAY": {
        "description": "Biological pathways and processes",
        "examples": ["glycolysis", "apoptosis", "oxidative phosphorylation"]
    },
    "SYMPTOM": {
        "description": "Clinical manifestations and symptoms of diseases",
        "examples": ["fever", "cough", "fatigue"]
    },
    "ANATOMY": {
        "description": "Anatomical structures, organs, and body parts",
        "examples": ["liver", "brain", "heart"]
    },
    "ORGANISM": {
        "description": "Living organisms including bacteria, viruses, and other pathogens",
        "examples": ["SARS-CoV-2", "E. coli", "S. aureus"]
    },
    "CHEMICAL": {
        "description": "Chemical compounds and substances not classified as drugs",
        "examples": ["glucose", "sodium chloride", "ATP"]
    },
    "METHOD": {
        "description": "Research methods, techniques, and procedures",
        "examples": ["PCR", "mass spectrometry", "CRISPR"]
    },
    "CELL_TYPE": {
        "description": "Types of cells in organisms",
        "examples": ["T cell", "hepatocyte", "neuron"]
    },
    "METABOLITE": {
        "description": "Small molecules that are intermediates or products of metabolism",
        "examples": ["lactate", "pyruvate", "citrate"]
    },
    "BIOLOGICAL_PROCESS": {
        "description": "Processes occurring at the cellular or molecular level in living organisms",
        "examples": ["inflammation", "methylation", "phosphorylation"]
    },
    "CLINICAL_FEATURE": {
        "description": "Clinical characteristics, phenotypes, or traits",
        "examples": ["hypertension", "obesity", "tachycardia"]
    }
}

# Define relationship types for the biomedical knowledge graph
RELATION_TYPES = {
    "TREATS": {
        "description": "Indicates that one entity (typically a drug) is used to treat another entity (typically a disease)",
        "subject_types": ["DRUG", "METHOD"],
        "object_types": ["DISEASE", "SYMPTOM", "CLINICAL_FEATURE"],
        "examples": [("aspirin", "TREATS", "headache")]
    },
    "CAUSES": {
        "description": "Indicates that one entity causes or contributes to another entity",
        "subject_types": ["DRUG", "GENE", "ORGANISM", "CHEMICAL", "METABOLITE"],
        "object_types": ["DISEASE", "SYMPTOM", "PROTEIN", "CLINICAL_FEATURE"],
        "examples": [("smoking", "CAUSES", "lung cancer")]
    },
    "INTERACTS_WITH": {
        "description": "Indicates interaction between two entities (e.g., drug-drug interactions, protein-protein interactions)",
        "subject_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL", "METABOLITE"],
        "object_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL", "METABOLITE"],
        "examples": [("warfarin", "INTERACTS_WITH", "aspirin")]
    },
    "ASSOCIATED_WITH": {
        "description": "Indicates a general association between entities without specifying directionality",
        "subject_types": ["any"],
        "object_types": ["any"],
        "examples": [("APOE4", "ASSOCIATED_WITH", "Alzheimer's disease")]
    },
    "PART_OF": {
        "description": "Indicates that one entity is a component or part of another entity",
        "subject_types": ["ANATOMY", "PROTEIN", "GENE", "CHEMICAL", "METABOLITE", "CELL_TYPE"],
        "object_types": ["ANATOMY", "PATHWAY", "PROTEIN", "BIOLOGICAL_PROCESS"],
        "examples": [("mitochondria", "PART_OF", "cell")]
    },
    "EXPRESSED_IN": {
        "description": "Indicates that a gene or protein is expressed in a specific anatomical location",
        "subject_types": ["GENE", "PROTEIN"],
        "object_types": ["ANATOMY", "CELL_TYPE"],
        "examples": [("insulin", "EXPRESSED_IN", "pancreas")]
    },
    "INHIBITS": {
        "description": "Indicates that one entity inhibits or suppresses another entity",
        "subject_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL", "METABOLITE"],
        "object_types": ["PROTEIN", "GENE", "PATHWAY", "BIOLOGICAL_PROCESS"],
        "examples": [("sildenafil", "INHIBITS", "PDE5")]
    },
    "ACTIVATES": {
        "description": "Indicates that one entity activates or enhances another entity",
        "subject_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL", "METABOLITE"],
        "object_types": ["PROTEIN", "GENE", "PATHWAY", "BIOLOGICAL_PROCESS"],
        "examples": [("insulin", "ACTIVATES", "insulin receptor")]
    },
    "CONVERTS_TO": {
        "description": "Indicates that one entity is converted into another entity",
        "subject_types": ["CHEMICAL", "DRUG", "METABOLITE"],
        "object_types": ["CHEMICAL", "DRUG", "METABOLITE"],
        "examples": [("tryptophan", "CONVERTS_TO", "serotonin")]
    },
    "COOCCURS_WITH": {
        "description": "Indicates co-occurrence or correlation between entities without implying causation",
        "subject_types": ["any"],
        "object_types": ["any"],
        "examples": [("diabetes", "COOCCURS_WITH", "hypertension")]
    },
    "BIOMARKER_FOR": {
        "description": "Indicates that one entity serves as a biomarker for a condition or state",
        "subject_types": ["PROTEIN", "GENE", "CHEMICAL", "METABOLITE"],
        "object_types": ["DISEASE", "CLINICAL_FEATURE", "BIOLOGICAL_PROCESS"],
        "examples": [("HbA1c", "BIOMARKER_FOR", "diabetes")]
    },
    "REGULATES": {
        "description": "Indicates that one entity regulates another without specifying activation or inhibition",
        "subject_types": ["GENE", "PROTEIN", "DRUG", "CHEMICAL", "METABOLITE"],
        "object_types": ["GENE", "PROTEIN", "PATHWAY", "BIOLOGICAL_PROCESS"],
        "examples": [("p53", "REGULATES", "cell cycle")]
    },
    "METABOLIZED_BY": {
        "description": "Indicates that one entity is metabolized by another",
        "subject_types": ["DRUG", "CHEMICAL", "METABOLITE"],
        "object_types": ["PROTEIN", "GENE", "PATHWAY"],
        "examples": [("caffeine", "METABOLIZED_BY", "CYP1A2")]
    },
    "USED_IN": {
        "description": "Indicates that one entity is used in or as part of another, particularly for methods",
        "subject_types": ["METHOD", "CHEMICAL", "DRUG"],
        "object_types": ["METHOD", "BIOLOGICAL_PROCESS"],
        "examples": [("chromatography", "USED_IN", "metabolomics")]
    }
}

def get_all_entity_types():
    """
    Get a list of all entity types defined in the schema.
    
    Returns:
        list: List of entity type names
    """
    return list(ENTITY_TYPES.keys())

def get_all_relation_types():
    """
    Get a list of all relation types defined in the schema.
    
    Returns:
        list: List of relation type names
    """
    return list(RELATION_TYPES.keys())

def get_entity_description(entity_type):
    """
    Get the description for a specific entity type.
    
    Args:
        entity_type (str): The entity type name
        
    Returns:
        str: Description of the entity type or None if not found
    """
    if entity_type in ENTITY_TYPES:
        return ENTITY_TYPES[entity_type]["description"]
    return None

def get_relation_description(relation_type):
    """
    Get the description for a specific relation type.
    
    Args:
        relation_type (str): The relation type name
        
    Returns:
        str: Description of the relation type or None if not found
    """
    if relation_type in RELATION_TYPES:
        return RELATION_TYPES[relation_type]["description"]
    return None

def is_valid_relation(subject_type, relation_type, object_type):
    """
    Check if a relation between two entity types is valid according to the schema.
    
    Args:
        subject_type (str): Type of the subject entity
        relation_type (str): Type of the relation
        object_type (str): Type of the object entity
        
    Returns:
        bool: True if the relation is valid, False otherwise
    """
    if relation_type not in RELATION_TYPES:
        return False
        
    subject_valid = (RELATION_TYPES[relation_type]["subject_types"] == ["any"] or 
                     subject_type in RELATION_TYPES[relation_type]["subject_types"])
                     
    object_valid = (RELATION_TYPES[relation_type]["object_types"] == ["any"] or 
                    object_type in RELATION_TYPES[relation_type]["object_types"])
                    
    return subject_valid and object_valid

def is_valid_entity_type(entity_type):
    """
    Check if an entity type is valid according to the schema.
    
    Args:
        entity_type (str): Entity type to check
        
    Returns:
        bool: True if the entity type is valid, False otherwise
    """
    return entity_type in ENTITY_TYPES

def get_valid_relation_types_between(subject_type, object_type):
    """
    Get all valid relation types that can exist between two entity types.
    
    Args:
        subject_type (str): Type of the subject entity
        object_type (str): Type of the object entity
        
    Returns:
        list: List of valid relation type names
    """
    valid_relations = []
    
    for rel_type, rel_data in RELATION_TYPES.items():
        subject_valid = (rel_data["subject_types"] == ["any"] or 
                         subject_type in rel_data["subject_types"])
        
        object_valid = (rel_data["object_types"] == ["any"] or 
                        object_type in rel_data["object_types"])
                        
        if subject_valid and object_valid:
            valid_relations.append(rel_type)
    
    return valid_relations

def get_entity_examples(entity_type):
    """
    Get examples for a specific entity type.
    
    Args:
        entity_type (str): The entity type name
        
    Returns:
        list: List of examples or empty list if not found
    """
    if entity_type in ENTITY_TYPES:
        return ENTITY_TYPES[entity_type].get("examples", [])
    return []

def get_relation_example(relation_type):
    """
    Get an example for a specific relation type.
    
    Args:
        relation_type (str): The relation type name
        
    Returns:
        tuple or None: Example tuple (subject, relation, object) or None if not found
    """
    if relation_type in RELATION_TYPES and "examples" in RELATION_TYPES[relation_type]:
        examples = RELATION_TYPES[relation_type]["examples"]
        if examples:
            return examples[0]
    return None

def get_relation_subject_types(relation_type):
    """
    Get valid subject entity types for a specific relation type.
    
    Args:
        relation_type (str): The relation type name
        
    Returns:
        list: List of valid subject entity types or empty list if not found
    """
    if relation_type in RELATION_TYPES:
        return RELATION_TYPES[relation_type].get("subject_types", [])
    return []

def get_relation_object_types(relation_type):
    """
    Get valid object entity types for a specific relation type.
    
    Args:
        relation_type (str): The relation type name
        
    Returns:
        list: List of valid object entity types or empty list if not found
    """
    if relation_type in RELATION_TYPES:
        return RELATION_TYPES[relation_type].get("object_types", [])
    return []
