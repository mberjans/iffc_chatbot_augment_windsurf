"""
Knowledge Graph Builder Module

This module provides functionality to build a knowledge graph from PubMed XML data
using entity and relation extraction, and maintains mutual indexing between
knowledge graph nodes/edges and source text.
"""

import os
import json
import datetime
import networkx as nx
from pathlib import Path

from data_preparation.pubmed_xml_parser import parse_pubmed_xml
from knowledge_augmentation.entity_extraction import extract_entities_from_parsed_xml
from knowledge_augmentation.relation_extraction import extract_relations_from_parsed_xml, generate_entity_id

def create_knowledge_graph():
    """
    Create a new empty NetworkX knowledge graph with appropriate attributes.
    
    Returns:
        nx.MultiDiGraph: A directed multigraph for the knowledge graph
    """
    # Using MultiDiGraph to allow multiple relationships between the same nodes
    kg = nx.MultiDiGraph()
    
    # Add graph-level metadata
    kg.graph['created'] = datetime.datetime.now().isoformat()
    kg.graph['version'] = '1.0'
    kg.graph['description'] = 'Biomedical Knowledge Graph from PubMed XML'
    
    return kg

def add_entity_to_graph(kg, entity):
    """
    Add an entity to the knowledge graph.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        entity (dict): Entity information
        
    Returns:
        str: ID of the added entity node
    """
    entity_id = generate_entity_id(entity)
    
    # Check if entity already exists
    if not kg.has_node(entity_id):
        kg.add_node(entity_id, 
                    type=entity['type'],
                    text=entity['text'],
                    normalized_text=entity['normalized_text'],
                    sources=[])
    
    return entity_id

def add_relation_to_graph(kg, relation):
    """
    Add a relation to the knowledge graph.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        relation (dict): Relation information
        
    Returns:
        tuple: Edge identifier (source_id, target_id, key)
    """
    subject_id = relation['subject']['id']
    object_id = relation['object']['id']
    predicate = relation['predicate']
    
    # Ensure nodes exist
    if not kg.has_node(subject_id):
        kg.add_node(subject_id, 
                    type=relation['subject']['type'],
                    text=relation['subject']['text'],
                    sources=[])
    
    if not kg.has_node(object_id):
        kg.add_node(object_id, 
                    type=relation['object']['type'],
                    text=relation['object']['text'],
                    sources=[])
    
    # Add edge with attributes
    edge_data = {
        'type': predicate,
        'evidence': relation['evidence'],
        'confidence': relation['confidence'],
        'sources': []
    }
    
    # MultiDiGraph allows multiple edges - add new edge and get key
    key = kg.add_edge(subject_id, object_id, **edge_data)
    
    return (subject_id, object_id, key)

def create_text_source_reference(pubmed_id, section, position=None):
    """
    Create a reference to a text source.
    
    Args:
        pubmed_id (str): PubMed ID of the article
        section (str): Section name
        position (dict, optional): Position information
        
    Returns:
        dict: Source reference
    """
    source_ref = {
        'pubmed_id': pubmed_id,
        'section': section,
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    if position:
        source_ref['start_pos'] = position.get('start_pos')
        source_ref['end_pos'] = position.get('end_pos')
    
    return source_ref

def add_source_to_entity(kg, entity_id, source_ref):
    """
    Add a source reference to an entity.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        entity_id (str): Entity ID
        source_ref (dict): Source reference
    """
    if kg.has_node(entity_id):
        kg.nodes[entity_id]['sources'].append(source_ref)

def add_source_to_relation(kg, subject_id, object_id, key, source_ref):
    """
    Add a source reference to a relation.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        subject_id (str): Subject entity ID
        object_id (str): Object entity ID
        key (int): Edge key
        source_ref (dict): Source reference
    """
    if kg.has_edge(subject_id, object_id, key):
        kg[subject_id][object_id][key]['sources'].append(source_ref)

def build_knowledge_graph_from_parsed_xml(parsed_data, pubmed_id, kg=None):
    """
    Build a knowledge graph from parsed PubMed XML data.
    
    Args:
        parsed_data (dict): Parsed PubMed XML data
        pubmed_id (str): PubMed ID
        kg (nx.MultiDiGraph, optional): Existing knowledge graph to update
        
    Returns:
        tuple: (knowledge graph, entities dict, relations dict)
    """
    # Create a new knowledge graph if none provided
    if kg is None:
        kg = create_knowledge_graph()
    
    # Extract entities and relations
    extracted_entities = extract_entities_from_parsed_xml(parsed_data)
    extracted_relations = extract_relations_from_parsed_xml(parsed_data, extracted_entities)
    
    # Process entities
    for section_name, entities in extracted_entities.get('entities', {}).items():
        for entity in entities:
            entity_id = add_entity_to_graph(kg, entity)
            source_ref = create_text_source_reference(
                pubmed_id, 
                section_name, 
                {'start_pos': entity.get('start_pos'), 'end_pos': entity.get('end_pos')}
            )
            add_source_to_entity(kg, entity_id, source_ref)
    
    # Process relations
    for section_name, relations in extracted_relations.get('relations', {}).items():
        for relation in relations:
            edge_info = add_relation_to_graph(kg, relation)
            source_ref = create_text_source_reference(pubmed_id, section_name)
            add_source_to_relation(kg, *edge_info, source_ref)
    
    return kg, extracted_entities, extracted_relations

def build_kg_from_pubmed_xml_file(xml_file_path, kg=None):
    """
    Build a knowledge graph directly from a PubMed XML file.
    
    Args:
        xml_file_path (str): Path to PubMed XML file
        kg (nx.MultiDiGraph, optional): Existing knowledge graph to update
        
    Returns:
        tuple: (knowledge graph, pubmed_id, parsed_data)
    """
    # Parse the XML file
    parsed_data = parse_pubmed_xml(xml_file_path)
    
    # Extract PubMed ID from metadata
    pubmed_id = parsed_data.get('metadata', {}).get('pmid', 'unknown')
    
    # Build knowledge graph
    kg, entities, relations = build_knowledge_graph_from_parsed_xml(parsed_data, pubmed_id, kg)
    
    return kg, pubmed_id, parsed_data

def save_knowledge_graph(kg, output_path):
    """
    Save the knowledge graph to a file.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        output_path (str): Output file path
        
    Returns:
        bool: Success status
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert NetworkX graph to JSON-serializable format
        data = nx.node_link_data(kg)
        
        # Add metadata
        data['metadata'] = {
            'saved_at': datetime.datetime.now().isoformat(),
            'node_count': kg.number_of_nodes(),
            'edge_count': kg.number_of_edges()
        }
        
        # Save the file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving knowledge graph: {e}")
        return False

def load_knowledge_graph(input_path):
    """
    Load a knowledge graph from a file.
    
    Args:
        input_path (str): Input file path
        
    Returns:
        nx.MultiDiGraph: Loaded knowledge graph or None if error
    """
    try:
        if not os.path.exists(input_path):
            print(f"Knowledge graph file not found: {input_path}")
            return None
            
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert from JSON format to NetworkX graph
        kg = nx.node_link_graph(data, directed=True, multigraph=True)
        
        return kg
    except Exception as e:
        print(f"Error loading knowledge graph: {e}")
        return None

def query_kg_by_entity(kg, entity_text, entity_type=None):
    """
    Query knowledge graph for nodes matching an entity text.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        entity_text (str): Entity text to search for
        entity_type (str, optional): Entity type to filter by
        
    Returns:
        list: Matching node IDs
    """
    matching_nodes = []
    
    for node_id, data in kg.nodes(data=True):
        if entity_text.lower() in data.get('text', '').lower() or entity_text.lower() in data.get('normalized_text', '').lower():
            if entity_type is None or data.get('type') == entity_type:
                matching_nodes.append(node_id)
    
    return matching_nodes

def get_entity_neighbors(kg, entity_id, relation_type=None):
    """
    Get neighbors of an entity in the knowledge graph.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        entity_id (str): Entity node ID
        relation_type (str, optional): Relation type to filter by
        
    Returns:
        list: Neighbor node data with relation information
    """
    if not kg.has_node(entity_id):
        return []
    
    neighbors = []
    
    # Outgoing relations (entity as subject)
    for _, target_id, key, edge_data in kg.out_edges(entity_id, data=True, keys=True):
        if relation_type is None or edge_data.get('type') == relation_type:
            target_data = kg.nodes[target_id]
            neighbors.append({
                'direction': 'outgoing',
                'relation_type': edge_data.get('type'),
                'entity_id': target_id,
                'entity_type': target_data.get('type'),
                'entity_text': target_data.get('text'),
                'confidence': edge_data.get('confidence', 0.0),
                'evidence': edge_data.get('evidence')
            })
    
    # Incoming relations (entity as object)
    for source_id, _, key, edge_data in kg.in_edges(entity_id, data=True, keys=True):
        if relation_type is None or edge_data.get('type') == relation_type:
            source_data = kg.nodes[source_id]
            neighbors.append({
                'direction': 'incoming',
                'relation_type': edge_data.get('type'),
                'entity_id': source_id,
                'entity_type': source_data.get('type'),
                'entity_text': source_data.get('text'),
                'confidence': edge_data.get('confidence', 0.0),
                'evidence': edge_data.get('evidence')
            })
    
    return neighbors

def get_entity_sources(kg, entity_id):
    """
    Get all source references for an entity.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        entity_id (str): Entity node ID
        
    Returns:
        list: Source references
    """
    if not kg.has_node(entity_id):
        return []
        
    return kg.nodes[entity_id].get('sources', [])

def get_relation_sources(kg, subject_id, object_id, key):
    """
    Get all source references for a relation.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        subject_id (str): Subject entity ID
        object_id (str): Object entity ID
        key (int): Edge key
        
    Returns:
        list: Source references
    """
    if not kg.has_edge(subject_id, object_id, key):
        return []
        
    return kg[subject_id][object_id][key].get('sources', [])

def get_kg_statistics(kg):
    """
    Get statistics about the knowledge graph.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph
        
    Returns:
        dict: Statistics
    """
    if kg is None:
        return {}
        
    # Count entities by type
    entity_types = {}
    for _, data in kg.nodes(data=True):
        entity_type = data.get('type', 'UNKNOWN')
        entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
    
    # Count relations by type
    relation_types = {}
    for _, _, data in kg.edges(data=True):
        relation_type = data.get('type', 'UNKNOWN')
        relation_types[relation_type] = relation_types.get(relation_type, 0) + 1
    
    # Count sources
    sources = set()
    for _, data in kg.nodes(data=True):
        for source in data.get('sources', []):
            if 'pubmed_id' in source:
                sources.add(source['pubmed_id'])
    
    return {
        'node_count': kg.number_of_nodes(),
        'edge_count': kg.number_of_edges(),
        'entity_types': entity_types,
        'relation_types': relation_types,
        'source_count': len(sources),
        'sources': list(sources)
    }
