"""
Relation Extraction Module

This module provides functions for extracting relationships between entities
in biomedical text using co-occurrence and pattern-based approaches.
"""

import re
from collections import defaultdict
from knowledge_augmentation.kg_schema import RELATION_TYPES, is_valid_relation
from knowledge_augmentation.entity_extraction import tokenize_sentences

# Define pattern matchers for different relation types
# These are simple pattern-based rules to identify relationships in text
RELATION_PATTERNS = {
    "TREATS": [
        r"(\w+)\s+(treat|treats|treating|treated|therapy|therapeutic|effective|efficacy|used for)\s+(\w+)",
        r"(\w+)\s+(for the treatment of|indicated for|used to treat)\s+(\w+)",
        r"treatment of (\w+) with (\w+)",
    ],
    "CAUSES": [
        r"(\w+)\s+(cause|causes|causing|caused|induce|induces|inducing|induced|lead to|leads to|leading to|led to)\s+(\w+)",
        r"(\w+)\s+(result in|results in|resulting in|resulted in)\s+(\w+)",
        r"(\w+)\s+(associated with|contributing to|contribute to|contributes to)\s+(\w+)",
    ],
    "INTERACTS_WITH": [
        r"(\w+)\s+(interact|interacts|interacting|interacted|interaction|binding|binds|bound|bind)\s+(with|to)\s+(\w+)",
        r"(\w+)-(\w+) interaction",
        r"(\w+)\s+(potentiate|potentiates|inhibit|inhibits)\s+(\w+)",
    ],
    "ASSOCIATED_WITH": [
        r"(\w+)\s+(associated with|linked to|related to|correlation with|correlate with|correlates with)\s+(\w+)",
        r"association between (\w+) and (\w+)",
        r"relationship between (\w+) and (\w+)",
    ],
    "PART_OF": [
        r"(\w+)\s+(is part of|are part of|component of|contained in|located in)\s+(\w+)",
        r"(\w+)\s+(contain|contains|containing|contained)\s+(\w+)",
    ],
    "EXPRESSED_IN": [
        r"(\w+)\s+(expressed in|expression in|expressed by|expression by|found in|localized in|localizes to)\s+(\w+)",
        r"expression of (\w+) in (\w+)",
    ],
    "INHIBITS": [
        r"(\w+)\s+(inhibit|inhibits|inhibiting|inhibited|suppress|suppresses|suppressing|suppressed|block|blocks|blocking|blocked)\s+(\w+)",
        r"inhibition of (\w+) by (\w+)",
    ],
    "ACTIVATES": [
        r"(\w+)\s+(activate|activates|activating|activated|stimulate|stimulates|stimulating|stimulated)\s+(\w+)",
        r"activation of (\w+) by (\w+)",
    ],
}

def find_sentence_with_entities(sentence, entity1, entity2):
    """
    Check if a sentence contains both entities.
    
    Args:
        sentence (str): The sentence to check
        entity1 (dict): First entity details
        entity2 (dict): Second entity details
        
    Returns:
        bool: True if both entities are in the sentence, False otherwise
    """
    sentence_lower = sentence.lower()
    return (entity1['normalized_text'] in sentence_lower and 
            entity2['normalized_text'] in sentence_lower)

def extract_relation_by_pattern(sentence, entity1, entity2):
    """
    Extract relation between two entities using pattern matching.
    
    Args:
        sentence (str): The sentence containing entities
        entity1 (dict): First entity details
        entity2 (dict): Second entity details
        
    Returns:
        str or None: The identified relation type or None
    """
    sentence_lower = sentence.lower()
    
    for relation_type, patterns in RELATION_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, sentence_lower)
            if matches:
                for match in matches:
                    # Handle different pattern types (tuple sizes)
                    if isinstance(match, tuple):
                        # For patterns with subject and object
                        if len(match) >= 3:
                            subject, _, obj = match[0], match[1], match[2]
                            if (entity1['normalized_text'] in subject and entity2['normalized_text'] in obj):
                                if is_valid_relation(entity1['type'], relation_type, entity2['type']):
                                    return relation_type, True  # Direction: entity1 -> entity2
                            elif (entity2['normalized_text'] in subject and entity1['normalized_text'] in obj):
                                if is_valid_relation(entity2['type'], relation_type, entity1['type']):
                                    return relation_type, False  # Direction: entity2 -> entity1
                        # For patterns like "interaction between X and Y"
                        elif len(match) >= 2:
                            term1, term2 = match[0], match[1]
                            if ((entity1['normalized_text'] in term1 and entity2['normalized_text'] in term2) or
                                (entity2['normalized_text'] in term1 and entity1['normalized_text'] in term2)):
                                return relation_type, True  # Default direction
                    else:  # Single string match
                        # Default cooccurrence relation if explicit pattern matched
                        return "ASSOCIATED_WITH", True
    
    return None, True

def extract_relations_by_cooccurrence(text, entities, window_size=2):
    """
    Extract relations between entities based on sentence co-occurrence.
    
    Args:
        text (str): Input text
        entities (list): List of extracted entities
        window_size (int): Number of sentences to consider for co-occurrence
        
    Returns:
        list: List of extracted relations
    """
    if not text or not entities:
        return []
    
    # Group entities by sentence
    sentences = tokenize_sentences(text)
    entity_pairs = []
    relations = []
    
    # Find all entity pairs in nearby sentences
    for i, sentence in enumerate(sentences):
        # Find entities in current sentence
        current_entities = [e for e in entities if e['normalized_text'] in sentence.lower()]
        
        # Skip if fewer than 2 entities in sentence
        if len(current_entities) < 2:
            continue
        
        # Create all possible entity pairs within the sentence
        for j in range(len(current_entities)):
            for k in range(j + 1, len(current_entities)):
                entity1 = current_entities[j]
                entity2 = current_entities[k]
                
                # Skip if entities are the same
                if entity1['text'] == entity2['text']:
                    continue
                
                entity_pairs.append((entity1, entity2, sentence))
    
    # Process entity pairs to extract relations
    for entity1, entity2, sentence in entity_pairs:
        # Try pattern matching first
        relation_type, direction = extract_relation_by_pattern(sentence, entity1, entity2)
        
        # If no pattern match, default to co-occurrence
        if relation_type is None:
            relation_type = "COOCCURS_WITH"
            direction = True  # Default direction
        
        # Determine subject and object based on direction
        if direction:
            subject, object_ = entity1, entity2
        else:
            subject, object_ = entity2, entity1
            
        # Check if the relation is valid according to schema
        if not is_valid_relation(subject['type'], relation_type, object_['type']):
            relation_type = "COOCCURS_WITH"  # Fallback to generic relation
            
        relation = {
            'subject': {
                'id': generate_entity_id(subject),
                'text': subject['text'],
                'type': subject['type']
            },
            'predicate': relation_type,
            'object': {
                'id': generate_entity_id(object_),
                'text': object_['text'],
                'type': object_['type']
            },
            'evidence': sentence,
            'confidence': 0.7 if relation_type != "COOCCURS_WITH" else 0.5
        }
        
        relations.append(relation)
    
    return relations

def generate_entity_id(entity):
    """
    Generate a unique ID for an entity.
    
    Args:
        entity (dict): Entity information
        
    Returns:
        str: Unique entity ID
    """
    return f"{entity['type']}:{entity['normalized_text']}"

def extract_relations_from_sections(sections, entities_by_section):
    """
    Extract relations from article sections using extracted entities.
    
    Args:
        sections (dict): Dictionary of article sections
        entities_by_section (dict): Dictionary of entities by section
        
    Returns:
        dict: Dictionary of relations by section
    """
    if not sections or not entities_by_section:
        return {}
        
    relations_by_section = {}
    
    for section_name, section_text in sections.items():
        if section_name not in entities_by_section:
            continue
            
        entities = entities_by_section[section_name]
        if not entities:
            continue
            
        relations = extract_relations_by_cooccurrence(section_text, entities)
        relations_by_section[section_name] = relations
    
    return relations_by_section

def extract_relations_from_parsed_xml(parsed_data, extracted_entities):
    """
    Extract relations from parsed PubMed XML data using extracted entities.
    
    Args:
        parsed_data (dict): Parsed PubMed XML data
        extracted_entities (dict): Dictionary of extracted entities by section
        
    Returns:
        dict: Dictionary with extracted relations by section
    """
    if not parsed_data or not extracted_entities:
        return {'relations': {}}
        
    result = {'relations': {}}
    
    # Extract relations from abstract
    abstract = parsed_data.get('abstract', '')
    if abstract and 'abstract' in extracted_entities.get('entities', {}):
        entities = extracted_entities['entities']['abstract']
        result['relations']['abstract'] = extract_relations_by_cooccurrence(abstract, entities)
    
    # Extract relations from sections
    sections = parsed_data.get('sections', {})
    if sections:
        for section_name, section_text in sections.items():
            if section_name in extracted_entities.get('entities', {}):
                entities = extracted_entities['entities'][section_name]
                result['relations'][section_name] = extract_relations_by_cooccurrence(section_text, entities)
    
    # Extract relations from full text if no sections available
    if not sections and 'full_text' in parsed_data and 'full_text' in extracted_entities.get('entities', {}):
        entities = extracted_entities['entities']['full_text']
        result['relations']['full_text'] = extract_relations_by_cooccurrence(parsed_data['full_text'], entities)
    
    return result
