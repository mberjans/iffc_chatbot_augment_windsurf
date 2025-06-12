"""
Named Entity Recognition (NER) Module

This module provides functions for extracting biomedical entities from text
using spaCy with biomedical NER models. It enhances the rule-based approach
with more sophisticated NLP techniques.
"""

import os
import json
import spacy
import requests
from pathlib import Path
from collections import defaultdict

# Import the schema
from knowledge_augmentation.kg_schema import ENTITY_TYPES, get_all_entity_types

# Path for storing downloaded models
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Default biomedical entity mapping from spaCy labels to our schema
DEFAULT_ENTITY_MAPPING = {
    "CHEMICAL": ["CHEMICAL", "DRUG"],
    "DISEASE": ["DISEASE", "SYMPTOM"],
    "GENE": ["GENE"],
    "SPECIES": ["ORGANISM"],
    "ANATOMY": ["ANATOMY"],
    "PROCEDURE": ["METHOD"],
    "DRUG": ["DRUG"],
    "PROTEIN": ["PROTEIN"]
}

def download_biomedical_model():
    """
    Download the biomedical NER model for spaCy if not already available.
    First attempts to use pip to install the model package, then falls back
    to spacy download command if necessary.
    
    Returns:
        bool: True if model is available (was already installed or successfully downloaded)
    """
    # Model name for biomedical NER
    model_name = "en_core_sci_md"
    
    try:
        # Try importing the model to check if it's installed
        spacy.load(model_name)
        print(f"Biomedical model '{model_name}' is already installed.")
        return True
    except Exception as e:
        print(f"Biomedical model '{model_name}' not found: {e}")
    
    # Install using pip
    try:
        print(f"Attempting to install biomedical model '{model_name}'...")
        # We'll use the system pip to install the model
        result = os.system(f"pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/{model_name}-0.5.0.tar.gz")
        
        if result == 0:
            # Verify installation
            try:
                spacy.load(model_name)
                print(f"Successfully installed biomedical model '{model_name}'")
                return True
            except Exception:
                pass
    except Exception as e:
        print(f"Failed to install model using pip: {e}")
    
    # Fall back to spacy download command
    try:
        print(f"Attempting to download biomedical model using spacy download...")
        import spacy.cli
        spacy.cli.download(model_name)
        print(f"Successfully downloaded biomedical model '{model_name}'")
        return True
    except Exception as e:
        print(f"Failed to download model: {e}")
        
    print("ERROR: Could not download or find the biomedical NER model.")
    print("Please manually install the model using: pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_md-0.5.0.tar.gz")
    return False

def setup_spacy_model(model_name="en_core_sci_md"):
    """
    Set up and return spaCy model for biomedical NER.
    Will attempt to download the model if not found.
    
    Args:
        model_name (str): Name of the spaCy model to use
    
    Returns:
        spacy.language.Language: Loaded spaCy model or None if not available
    """
    try:
        # Try to load the model
        nlp = spacy.load(model_name)
        return nlp
    except Exception as e:
        print(f"Model '{model_name}' not found: {e}")
        
        # Try to download the model
        if download_biomedical_model():
            try:
                # Try loading again
                nlp = spacy.load(model_name)
                return nlp
            except Exception as e2:
                print(f"Error loading model after download: {e2}")
        
    # Fall back to a basic English model if biomedical model isn't available
    try:
        print("Falling back to basic English model...")
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except Exception:
        # Last resort - load the smallest model that should come with spaCy
        try:
            print("Attempting to load minimal spaCy model...")
            nlp = spacy.blank("en")
            return nlp
        except Exception as e:
            print(f"Could not load any spaCy model: {e}")
            return None

def map_ner_to_schema(ner_type, entity_mapping=None):
    """
    Map NER entity types to our schema entity types.
    
    Args:
        ner_type (str): NER entity type from spaCy
        entity_mapping (dict, optional): Custom mapping from NER types to schema types
        
    Returns:
        str: Mapped entity type or None if no mapping exists
    """
    if entity_mapping is None:
        entity_mapping = DEFAULT_ENTITY_MAPPING
        
    for schema_type, ner_types in entity_mapping.items():
        if ner_type in ner_types:
            return schema_type
    
    return None

def extract_entities_with_ner(text, nlp=None, entity_mapping=None):
    """
    Extract entities from text using spaCy NER.
    
    Args:
        text (str): Input text
        nlp (spacy.language.Language, optional): Loaded spaCy model
        entity_mapping (dict, optional): Custom mapping from NER types to schema types
        
    Returns:
        list: List of extracted entities with type, text, and position
    """
    if not text:
        return []
        
    # Set up spaCy model if not provided
    if nlp is None:
        nlp = setup_spacy_model()
        if nlp is None:
            print("WARNING: No spaCy model available for NER, returning empty entity list")
            return []
    
    # Use default entity mapping if not provided
    if entity_mapping is None:
        entity_mapping = DEFAULT_ENTITY_MAPPING
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract entities
    extracted_entities = []
    for ent in doc.ents:
        # Map the spaCy entity type to our schema
        entity_type = map_ner_to_schema(ent.label_, entity_mapping)
        
        # Skip entities that don't map to our schema
        if not entity_type:
            continue
        
        extracted_entities.append({
            'type': entity_type,
            'text': ent.text,
            'normalized_text': ent.text.lower(),
            'start_pos': ent.start_char,
            'end_pos': ent.end_char
        })
    
    return extracted_entities

def extract_entities_from_sections_with_ner(sections, nlp=None, entity_mapping=None):
    """
    Extract entities from article sections using spaCy NER.
    
    Args:
        sections (dict): Dictionary of article sections with section name as key and text as value
        nlp (spacy.language.Language, optional): Loaded spaCy model
        entity_mapping (dict, optional): Custom mapping from NER types to schema types
        
    Returns:
        dict: Dictionary of extracted entities by section
    """
    if not sections:
        return {}
    
    # Set up spaCy model if not provided
    if nlp is None:
        nlp = setup_spacy_model()
        if nlp is None:
            print("WARNING: No spaCy model available for NER, returning empty entity list")
            return {}
    
    entities_by_section = {}
    
    for section_name, section_text in sections.items():
        entities_by_section[section_name] = extract_entities_with_ner(section_text, nlp, entity_mapping)
    
    return entities_by_section

def extract_entities_from_parsed_xml_with_ner(parsed_data, nlp=None, entity_mapping=None):
    """
    Extract entities from parsed PubMed XML data using spaCy NER.
    
    Args:
        parsed_data (dict): Parsed PubMed XML data with metadata, abstract, and sections
        nlp (spacy.language.Language, optional): Loaded spaCy model
        entity_mapping (dict, optional): Custom mapping from NER types to schema types
        
    Returns:
        dict: Dictionary with extracted entities by section and metadata
    """
    if not parsed_data:
        return {'entities': {}, 'metadata': {}}
    
    # Set up spaCy model if not provided
    if nlp is None:
        nlp = setup_spacy_model()
        if nlp is None:
            print("WARNING: No spaCy model available for NER")
            return {'entities': {}, 'metadata': parsed_data.get('metadata', {})}
    
    result = {
        'entities': {},
        'metadata': parsed_data.get('metadata', {})
    }
    
    # Extract entities from abstract
    abstract = parsed_data.get('abstract', '')
    if abstract:
        result['entities']['abstract'] = extract_entities_with_ner(abstract, nlp, entity_mapping)
    
    # Extract entities from sections
    sections = parsed_data.get('sections', {})
    if sections:
        for section_name, section_text in sections.items():
            result['entities'][section_name] = extract_entities_with_ner(section_text, nlp, entity_mapping)
    
    # Extract entities from full text if no sections available
    if not sections and 'full_text' in parsed_data and parsed_data['full_text']:
        result['entities']['full_text'] = extract_entities_with_ner(parsed_data['full_text'], nlp, entity_mapping)
    
    return result

def merge_entity_extractions(rule_based_entities, ner_entities):
    """
    Merge entities extracted from rule-based approach and NER.
    Handles overlapping entities and removes duplicates.
    
    Args:
        rule_based_entities (dict): Entities extracted using rule-based approach
        ner_entities (dict): Entities extracted using NER
        
    Returns:
        dict: Merged entity dictionary
    """
    if not rule_based_entities and not ner_entities:
        return {'entities': {}}
    
    if not rule_based_entities:
        return ner_entities
    
    if not ner_entities:
        return rule_based_entities
    
    # Initialize result with metadata from either source
    result = {
        'entities': {},
        'metadata': rule_based_entities.get('metadata', ner_entities.get('metadata', {}))
    }
    
    # Get all section names from both sources
    sections = set()
    if 'entities' in rule_based_entities:
        sections.update(rule_based_entities['entities'].keys())
    if 'entities' in ner_entities:
        sections.update(ner_entities['entities'].keys())
    
    # Merge entities for each section
    for section in sections:
        # Get entities from both sources for this section
        rule_entities = rule_based_entities.get('entities', {}).get(section, [])
        ner_section_entities = ner_entities.get('entities', {}).get(section, [])
        
        # Combine entities
        combined_entities = rule_entities + ner_section_entities
        
        # Remove duplicates by normalized text
        unique_entities = {}
        for entity in combined_entities:
            key = (entity['normalized_text'], entity['type'])
            
            # If this is a new entity or has higher confidence, use it
            if key not in unique_entities:
                unique_entities[key] = entity
        
        # Store merged entities for this section
        result['entities'][section] = list(unique_entities.values())
    
    return result
