"""
Entity Extraction Module

This module provides functions for extracting biomedical entities from parsed PubMed XML
data. It leverages both the NER extractor and rule-based approaches for comprehensive
entity identification. Extracted entities are validated against the knowledge graph schema.
"""

import os
import json
from pathlib import Path
from collections import defaultdict

# Import schema and NER modules
from knowledge_augmentation.kg_schema import (
    ENTITY_TYPES, 
    is_valid_entity_type,
    get_entity_description
)
from knowledge_augmentation.ner_extractor import (
    setup_spacy_model,
    extract_entities_from_parsed_xml_with_ner,
    DEFAULT_ENTITY_MAPPING
)

# Directory for storing entity extraction patterns and dictionaries
ENTITY_DATA_DIR = os.path.join(os.path.dirname(__file__), 'entity_data')
os.makedirs(ENTITY_DATA_DIR, exist_ok=True)

# Default paths for entity dictionaries
ENTITY_DICTIONARIES = {
    'DRUG': os.path.join(ENTITY_DATA_DIR, 'drugs.json'),
    'DISEASE': os.path.join(ENTITY_DATA_DIR, 'diseases.json'),
    'GENE': os.path.join(ENTITY_DATA_DIR, 'genes.json'),
    'PROTEIN': os.path.join(ENTITY_DATA_DIR, 'proteins.json'),
}

def load_entity_dictionary(entity_type):
    """
    Load an entity dictionary from disk if available.
    
    Args:
        entity_type (str): Type of entity dictionary to load
        
    Returns:
        dict: Dictionary of entities with their normalized forms or empty dict if not found
    """
    if entity_type not in ENTITY_DICTIONARIES:
        return {}
        
    dict_path = ENTITY_DICTIONARIES[entity_type]
    
    if not os.path.exists(dict_path):
        return {}
        
    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading entity dictionary for {entity_type}: {e}")
        return {}

def normalize_entity_text(text):
    """
    Normalize entity text by converting to lowercase and removing excess whitespace.
    
    Args:
        text (str): Raw entity text
        
    Returns:
        str: Normalized entity text
    """
    if not text:
        return ""
        
    # Convert to lowercase
    normalized = text.lower()
    
    # Remove excess whitespace
    normalized = " ".join(normalized.split())
    
    return normalized

def extract_entities_with_dictionary(text, entity_type):
    """
    Extract entities using dictionary-based approach.
    
    Args:
        text (str): Input text to process
        entity_type (str): Type of entity to extract
        
    Returns:
        list: List of extracted entities with type, text, and position
    """
    if not text:
        return []
        
    entity_dict = load_entity_dictionary(entity_type)
    
    if not entity_dict:
        return []
        
    extracted_entities = []
    normalized_text = normalize_entity_text(text)
    
    # Iterate through each entity in the dictionary
    for entity_key, entity_data in entity_dict.items():
        entity_normalized = normalize_entity_text(entity_key)
        
        # Simple pattern matching (non-regex approach)
        start_pos = 0
        while start_pos < len(normalized_text):
            pos = normalized_text.find(entity_normalized, start_pos)
            if pos == -1:
                break
                
            # Get the original text from the position
            original_text = text[pos:pos + len(entity_key)]
            
            # Create entity entry
            extracted_entities.append({
                'type': entity_type,
                'text': original_text,
                'normalized_text': entity_normalized,
                'start_pos': pos,
                'end_pos': pos + len(entity_key),
                'source': 'dictionary'
            })
            
            start_pos = pos + len(entity_normalized)
    
    return extracted_entities

def extract_entities_with_rule_based(text, entity_types=None):
    """
    Extract entities using rule-based approach.
    
    Args:
        text (str): Input text to process
        entity_types (list, optional): List of entity types to extract
        
    Returns:
        list: List of extracted entities with type, text, and position
    """
    if not text:
        return []
        
    # Use all entity types if none specified
    if entity_types is None:
        entity_types = list(ENTITY_TYPES.keys())
        
    extracted_entities = []
    
    for entity_type in entity_types:
        # Extract entities for this type
        entities = extract_entities_with_dictionary(text, entity_type)
        extracted_entities.extend(entities)
    
    return extracted_entities

def extract_entities_from_parsed_xml(parsed_data, use_ner=True, use_rule_based=True):
    """
    Extract entities from parsed PubMed XML data using multiple approaches.
    
    Args:
        parsed_data (dict): Parsed PubMed XML data with metadata, abstract, and sections
        use_ner (bool): Whether to use NER-based extraction
        use_rule_based (bool): Whether to use rule-based extraction
        
    Returns:
        dict: Dictionary with extracted entities by section and metadata
    """
    if not parsed_data:
        return {'entities': {}, 'metadata': {}}
    
    # Initialize result structure
    result = {
        'entities': {},
        'metadata': parsed_data.get('metadata', {})
    }
    
    # Extract using NER if enabled
    ner_results = {}
    if use_ner:
        nlp = setup_spacy_model()
        ner_results = extract_entities_from_parsed_xml_with_ner(parsed_data, nlp)
    
    # Get sections to process
    sections = {}
    if 'abstract' in parsed_data and parsed_data['abstract']:
        sections['abstract'] = parsed_data['abstract']
        
    if 'sections' in parsed_data and parsed_data['sections']:
        sections.update(parsed_data['sections'])
    
    if not sections and 'full_text' in parsed_data and parsed_data['full_text']:
        sections['full_text'] = parsed_data['full_text']
    
    # Extract using rule-based approach if enabled
    if use_rule_based:
        for section_name, section_text in sections.items():
            rule_based_entities = extract_entities_with_rule_based(section_text)
            
            # Get existing NER entities for this section or initialize empty list
            ner_section_entities = ner_results.get('entities', {}).get(section_name, [])
            
            # Combine and deduplicate entities
            combined_entities = rule_based_entities + ner_section_entities
            
            # Remove duplicates
            unique_entities = {}
            for entity in combined_entities:
                key = (entity['normalized_text'], entity['type'])
                
                if key not in unique_entities:
                    unique_entities[key] = entity
                
            # Store final entities for this section
            result['entities'][section_name] = list(unique_entities.values())
    else:
        # Just use NER results
        result = ner_results
    
    # Apply validation to ensure all entities conform to schema
    for section_name, entities in result['entities'].items():
        valid_entities = []
        for entity in entities:
            if is_valid_entity_type(entity['type']):
                valid_entities.append(entity)
            else:
                # Try to map to a valid type
                for valid_type in ENTITY_TYPES:
                    if entity['type'].upper() == valid_type:
                        entity['type'] = valid_type
                        valid_entities.append(entity)
                        break
        
        result['entities'][section_name] = valid_entities
    
    return result

def get_entity_statistics(extracted_entities):
    """
    Calculate statistics about extracted entities.
    
    Args:
        extracted_entities (dict): Dictionary with extracted entities by section
        
    Returns:
        dict: Statistics about extracted entities
    """
    stats = {
        'total_entities': 0,
        'entities_by_type': defaultdict(int),
        'entities_by_section': defaultdict(int)
    }
    
    if not extracted_entities or 'entities' not in extracted_entities:
        return stats
    
    for section_name, entities in extracted_entities['entities'].items():
        section_count = len(entities)
        stats['total_entities'] += section_count
        stats['entities_by_section'][section_name] = section_count
        
        for entity in entities:
            entity_type = entity['type']
            stats['entities_by_type'][entity_type] += 1
    
    return stats

def merge_duplicate_entities(entities):
    """
    Merge duplicate entities with same normalized text and type.
    
    Args:
        entities (list): List of entity dictionaries
        
    Returns:
        list: Deduplicated list of entities
    """
    if not entities:
        return []
        
    unique_entities = {}
    
    for entity in entities:
        key = (entity.get('normalized_text', ''), entity.get('type', ''))
        
        if key not in unique_entities:
            unique_entities[key] = entity
    
    return list(unique_entities.values())
