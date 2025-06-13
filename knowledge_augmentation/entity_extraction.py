"""
Entity Extraction Module

This module provides functions for extracting biomedical entities from text
using rule-based approaches and NLTK for basic NLP tasks.
"""

import re
import json
import os

# Attempt to import NLTK and required resources, but gracefully fall back if
# the package or its data files are unavailable. This prevents runtime errors
# during environments where downloading NLTK data is not possible (e.g., CI).
try:
    import nltk  # type: ignore
    from nltk.tokenize import sent_tokenize, word_tokenize  # type: ignore
    from nltk.corpus import stopwords  # type: ignore
    from nltk.stem import WordNetLemmatizer  # type: ignore

    _nltk_ok = True

    # Ensure required corpora are available; otherwise trigger fallback.
    try:
        stop_words = set(stopwords.words("english"))
        import nltk.data as _nltk_data  # type: ignore
        _nltk_data.find("tokenizers/punkt")  # verify punkt resource exists
    except LookupError:
        _nltk_ok = False
except Exception:  # pragma: no cover – any error leads to fallback
    _nltk_ok = False

if not _nltk_ok:
    # -----------------------------
    # Minimal fallback replacements
    # -----------------------------
    def sent_tokenize(text):  # type: ignore
        """Very naive sentence splitter used when NLTK is unavailable."""
        if not text:
            return []
        return re.split(r"[.!?]\s+", text)

    def word_tokenize(text):  # type: ignore
        """Very naive word tokenizer used when NLTK is unavailable."""
        if not text:
            return []
        return re.findall(r"\b\w+\b", text.lower())

    stop_words = set()

    class _DummyLemmatizer:  # pylint: disable=too-few-public-methods
        """Simple lemmatizer that returns words unchanged."""

        def lemmatize(self, word):  # noqa: D401 – simple passthrough
            return word

    lemmatizer = _DummyLemmatizer()
else:
    # NLTK with data is available – initialise the standard lemmatizer.
    lemmatizer = WordNetLemmatizer()

# Import the schema
from knowledge_augmentation.kg_schema import ENTITY_TYPES, get_all_entity_types

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
    """Lightweight sentence splitter that avoids heavy NLTK dependencies."""
    if not text:
        return []
    # Split on period, exclamation, or question mark followed by whitespace
    return [s.strip() for s in re.split(r"[.!?]+\s+", text) if s.strip()]

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

def extract_relationships_cooccurrence(text_segment_normalized: str, entities_in_segment: list) -> list:
    """
    Extracts co-occurrence relationships between entities within the same sentence.

    Args:
        text_segment_normalized (str): The normalized text segment from which entities were extracted.
        entities_in_segment (list): A list of entity dictionaries found in this segment.
                                    Each entity dict should have 'text', 'type', 'start_pos', 'end_pos'.
                                    Positions must be relative to text_segment_normalized.

    Returns:
        list: A list of relationship dictionaries.
    """
    relationships = []
    if not text_segment_normalized or not entities_in_segment:
        return relationships

    tokenizer = sent_tokenize
    sentence_spans = []
    # Convert iterator to list to avoid issues if tokenizer is stateful or single-pass
    for sentence in tokenizer(text_segment_normalized):
        sentence_spans.append((text_segment_normalized.find(sentence), text_segment_normalized.find(sentence) + len(sentence)))

    for sent_start, sent_end in sentence_spans:
        sentence_text_normalized = text_segment_normalized[sent_start:sent_end]
        
        entities_in_sentence = []
        for entity in entities_in_segment:
            # Check if the entity is within the current sentence span
            if entity['start_pos'] >= sent_start and entity['end_pos'] <= sent_end:
                entities_in_sentence.append(entity)

        if len(entities_in_sentence) >= 2:
            # Generate pairs of entities in the sentence
            for i in range(len(entities_in_sentence)):
                for j in range(i + 1, len(entities_in_sentence)):
                    entity1 = entities_in_sentence[i]
                    entity2 = entities_in_sentence[j]
                    
                    # Ensure entities are not identical in text and type if that's a concern
                    # For co-occurrence, any two distinct entity mentions are usually fine

                    relation = {
                        'entity1_text': entity1['text'],
                        'entity1_type': entity1['type'],
                        'entity1_start_in_segment': entity1['start_pos'],
                        'entity1_end_in_segment': entity1['end_pos'],
                        'entity2_text': entity2['text'],
                        'entity2_type': entity2['type'],
                        'entity2_start_in_segment': entity2['start_pos'],
                        'entity2_end_in_segment': entity2['end_pos'],
                        'type': 'co-occurs_in_sentence',
                        'sentence_context_normalized': sentence_text_normalized
                    }
                    relationships.append(relation)
    
    return relationships

def extract_relationships_from_parsed_xml(parsed_xml_data: dict, extracted_entities_info: dict) -> dict:
    """
    Extracts co-occurrence relationships from different parts of parsed PubMed XML data.

    Args:
        parsed_xml_data (dict): Parsed PubMed XML data (output of a parser like pubmedparser2),
                                expected to contain 'abstract', 'sections', 'full_text'.
        extracted_entities_info (dict): Output from extract_entities_from_parsed_xml, containing
                                        entities categorized by text sections ('abstract', 'section_name', etc.).

    Returns:
        dict: A dictionary where keys are context names (e.g., 'abstract', 'section_name')
              and values are lists of relationship dictionaries found in that context.
    """
    relations_by_context = {}
    if not parsed_xml_data or not extracted_entities_info or 'entities' not in extracted_entities_info:
        return relations_by_context

    entities_by_section = extracted_entities_info['entities']

    # Helper to get original text for a given context (e.g., abstract, section_X)
    def get_original_text_for_context(context_name):
        if context_name == 'abstract':
            return parsed_xml_data.get('abstract')
        if parsed_xml_data.get('sections') and context_name in parsed_xml_data['sections']:
            return parsed_xml_data['sections'][context_name]
        if context_name == 'full_text': # Fallback if entities were extracted from 'full_text'
             return parsed_xml_data.get('full_text')
        return None

    for context_name, context_entities in entities_by_section.items():
        if not context_entities: # Skip if no entities in this context
            continue

        original_text_for_context = get_original_text_for_context(context_name)

        if original_text_for_context:
            # IMPORTANT: Normalize the text segment in the same way entity extraction did,
            # so that entity positions are valid for this normalized text.
            normalized_text_for_context = normalize_text(original_text_for_context)
            
            # The 'context_entities' already have positions relative to this 'normalized_text_for_context'
            # because they were generated by extract_entities_from_text(original_text_for_context, ...)
            # which internally normalizes and calculates positions against that.
            context_relations = extract_relationships_cooccurrence(normalized_text_for_context, context_entities)
            if context_relations:
                relations_by_context[context_name] = context_relations
                
    return relations_by_context
