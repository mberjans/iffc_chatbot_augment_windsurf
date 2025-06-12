"""
Entity Extraction Module

This module provides functions for extracting biomedical entities from text
using rule-based approaches and NLTK for basic NLP tasks.
"""

import re
import json
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Import the schema
from knowledge_augmentation.kg_schema import ENTITY_TYPES, get_all_entity_types

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Path for storing entity dictionaries/gazetteers
ENTITY_DICT_DIR = os.path.join(os.path.dirname(__file__), 'resources')
os.makedirs(ENTITY_DICT_DIR, exist_ok=True)

# Default dictionary paths
DEFAULT_ENTITY_DICT_PATHS = {
    entity_type: os.path.join(ENTITY_DICT_DIR, f"{entity_type.lower()}_dict.json")
    for entity_type in get_all_entity_types()
}

# Default entity dictionaries with examples from schema
DEFAULT_ENTITY_DICTS = {
    entity_type: ENTITY_TYPES[entity_type].get("examples", [])
    for entity_type in get_all_entity_types()
}

def normalize_text(text):
    """
    Normalize text by converting to lowercase, removing special characters, and excess whitespace.
    
    Args:
        text (str): Input text to normalize
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep hyphens for compound terms
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def tokenize_sentences(text):
    """
    Tokenize text into sentences.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences
    """
    if not text:
        return []
    
    return sent_tokenize(text)

def tokenize_words(text):
    """
    Tokenize text into words, removing stopwords and lemmatizing.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of processed tokens
    """
    if not text:
        return []
    
    # Tokenize
    tokens = word_tokenize(normalize_text(text))
    
    # Remove stopwords and apply lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and len(token) > 1]
    
    return tokens

def load_entity_dictionaries(dict_paths=None):
    """
    Load entity dictionaries from files or create defaults if not exists.
    
    Args:
        dict_paths (dict, optional): Dictionary mapping entity types to file paths
        
    Returns:
        dict: Dictionary of entity dictionaries by type
    """
    dict_paths = dict_paths or DEFAULT_ENTITY_DICT_PATHS
    entity_dicts = {}
    
    for entity_type, path in dict_paths.items():
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    entity_dicts[entity_type] = json.load(f)
            else:
                # Use default dictionary and save it
                entity_dicts[entity_type] = DEFAULT_ENTITY_DICTS.get(entity_type, [])
                save_entity_dictionary(entity_type, entity_dicts[entity_type])
        except Exception as e:
            print(f"Error loading entity dictionary for {entity_type}: {e}")
            entity_dicts[entity_type] = DEFAULT_ENTITY_DICTS.get(entity_type, [])
    
    return entity_dicts

def save_entity_dictionary(entity_type, entity_list, dict_path=None):
    """
    Save an entity dictionary to a file.
    
    Args:
        entity_type (str): The entity type
        entity_list (list): List of entities
        dict_path (str, optional): Path to save the dictionary
    """
    if dict_path is None:
        dict_path = DEFAULT_ENTITY_DICT_PATHS[entity_type]
    
    os.makedirs(os.path.dirname(dict_path), exist_ok=True)
    
    try:
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(entity_list, f, indent=2)
    except Exception as e:
        print(f"Error saving entity dictionary for {entity_type}: {e}")

def extract_entities_from_text(text, entity_dicts=None):
    """
    Extract entities from text using dictionary-based matching.
    
    Args:
        text (str): Input text
        entity_dicts (dict, optional): Dictionary of entity dictionaries by type
        
    Returns:
        list: List of extracted entities with type, text, and position
    """
    if not text:
        return []
    
    if entity_dicts is None:
        entity_dicts = load_entity_dictionaries()
    
    extracted_entities = []
    normalized_text = normalize_text(text)
    
    for entity_type, entities in entity_dicts.items():
        for entity in entities:
            entity_lower = entity.lower()
            
            # Find all occurrences of the entity in the text
            for match in re.finditer(r'\b' + re.escape(entity_lower) + r'\b', normalized_text):
                start_pos, end_pos = match.span()
                
                extracted_entities.append({
                    'type': entity_type,
                    'text': entity,
                    'normalized_text': entity_lower,
                    'start_pos': start_pos,
                    'end_pos': end_pos
                })
    
    # Sort entities by position
    extracted_entities.sort(key=lambda x: x['start_pos'])
    
    return extracted_entities

def extract_entities_from_sections(sections, entity_dicts=None):
    """
    Extract entities from article sections.
    
    Args:
        sections (dict): Dictionary of article sections with section name as key and text as value
        entity_dicts (dict, optional): Dictionary of entity dictionaries by type
        
    Returns:
        dict: Dictionary of extracted entities by section
    """
    if not sections:
        return {}
    
    if entity_dicts is None:
        entity_dicts = load_entity_dictionaries()
    
    entities_by_section = {}
    
    for section_name, section_text in sections.items():
        entities_by_section[section_name] = extract_entities_from_text(section_text, entity_dicts)
    
    return entities_by_section

def extract_entities_from_parsed_xml(parsed_data, entity_dicts=None):
    """
    Extract entities from parsed PubMed XML data.
    
    Args:
        parsed_data (dict): Parsed PubMed XML data with metadata, abstract, and sections
        entity_dicts (dict, optional): Dictionary of entity dictionaries by type
        
    Returns:
        dict: Dictionary with extracted entities by section and metadata
    """
    if not parsed_data:
        return {'entities': {}, 'metadata': {}}
    
    if entity_dicts is None:
        entity_dicts = load_entity_dictionaries()
    
    result = {
        'entities': {},
        'metadata': parsed_data.get('metadata', {})
    }
    
    # Extract entities from abstract
    abstract = parsed_data.get('abstract', '')
    if abstract:
        result['entities']['abstract'] = extract_entities_from_text(abstract, entity_dicts)
    
    # Extract entities from sections
    sections = parsed_data.get('sections', {})
    if sections:
        for section_name, section_text in sections.items():
            result['entities'][section_name] = extract_entities_from_text(section_text, entity_dicts)
    
    # Extract entities from full text if no sections available
    if not sections and 'full_text' in parsed_data and parsed_data['full_text']:
        result['entities']['full_text'] = extract_entities_from_text(parsed_data['full_text'], entity_dicts)
    
    return result
