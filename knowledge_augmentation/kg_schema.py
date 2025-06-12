"""
Knowledge Graph Schema Definition

This module defines the schema for the biomedical knowledge graph, including
entity types and relationship types.
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
    }
}

# Define relationship types for the biomedical knowledge graph
RELATION_TYPES = {
    "TREATS": {
        "description": "Indicates that one entity (typically a drug) is used to treat another entity (typically a disease)",
        "subject_types": ["DRUG", "METHOD"],
        "object_types": ["DISEASE", "SYMPTOM"],
        "examples": [("aspirin", "TREATS", "headache")]
    },
    "CAUSES": {
        "description": "Indicates that one entity causes or contributes to another entity",
        "subject_types": ["DRUG", "GENE", "ORGANISM", "CHEMICAL"],
        "object_types": ["DISEASE", "SYMPTOM", "PROTEIN"],
        "examples": [("smoking", "CAUSES", "lung cancer")]
    },
    "INTERACTS_WITH": {
        "description": "Indicates interaction between two entities (e.g., drug-drug interactions, protein-protein interactions)",
        "subject_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL"],
        "object_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL"],
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
        "subject_types": ["ANATOMY", "PROTEIN", "GENE", "CHEMICAL"],
        "object_types": ["ANATOMY", "PATHWAY", "PROTEIN"],
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
        "subject_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL"],
        "object_types": ["PROTEIN", "GENE", "PATHWAY"],
        "examples": [("sildenafil", "INHIBITS", "PDE5")]
    },
    "ACTIVATES": {
        "description": "Indicates that one entity activates or enhances another entity",
        "subject_types": ["DRUG", "PROTEIN", "GENE", "CHEMICAL"],
        "object_types": ["PROTEIN", "GENE", "PATHWAY"],
        "examples": [("insulin", "ACTIVATES", "insulin receptor")]
    },
    "CONVERTS_TO": {
        "description": "Indicates that one entity is converted into another entity",
        "subject_types": ["CHEMICAL", "DRUG"],
        "object_types": ["CHEMICAL", "DRUG"],
        "examples": [("tryptophan", "CONVERTS_TO", "serotonin")]
    },
    "COOCCURS_WITH": {
        "description": "Indicates co-occurrence or correlation between entities without implying causation",
        "subject_types": ["any"],
        "object_types": ["any"],
        "examples": [("diabetes", "COOCCURS_WITH", "hypertension")]
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
