"""
Build Knowledge Graph from PubMed XML

This script demonstrates how to build a knowledge graph from PubMed XML files.
"""

import os
import argparse
import networkx as nx
from pathlib import Path

from data_preparation.pubmed_xml_downloader import download_pubmed_xml, is_valid_pubmed_id
from knowledge_augmentation.kg_builder import (
    build_kg_from_pubmed_xml_file,
    save_knowledge_graph,
    load_knowledge_graph,
    get_kg_statistics
)

def process_pubmed_xml(pubmed_id, output_dir=None, kg_file=None):
    """
    Process a PubMed XML file to build/update a knowledge graph.
    
    Args:
        pubmed_id (str): PubMed ID
        output_dir (str): Output directory
        kg_file (str): Path to existing knowledge graph file
        
    Returns:
        tuple: (success status, knowledge graph, output path)
    """
    # Validate PubMed ID
    if not is_valid_pubmed_id(pubmed_id):
        print(f"Invalid PubMed ID: {pubmed_id}")
        return False, None, None
        
    # Set up output directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'knowledge_graphs')
    os.makedirs(output_dir, exist_ok=True)
    
    # Download PubMed XML
    xml_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'pubmed_xml')
    os.makedirs(xml_dir, exist_ok=True)
    
    xml_file = download_pubmed_xml(pubmed_id, output_path=xml_dir)
    if not xml_file or not os.path.exists(xml_file):
        print(f"Failed to download PubMed XML for ID: {pubmed_id}")
        return False, None, None
    
    # Load existing knowledge graph if provided
    kg = None
    if kg_file and os.path.exists(kg_file):
        kg = load_knowledge_graph(kg_file)
        print(f"Loaded existing knowledge graph from {kg_file}")
        print(f"Initial statistics: {get_kg_statistics(kg)}")
    
    # Build knowledge graph
    print(f"Building knowledge graph from {xml_file}...")
    kg, _, _ = build_kg_from_pubmed_xml_file(xml_file, kg)
    
    # Save knowledge graph
    if kg:
        output_file = os.path.join(output_dir, f"kg_{pubmed_id}.json")
        success = save_knowledge_graph(kg, output_file)
        
        if success:
            print(f"Knowledge graph saved to {output_file}")
            print(f"Final statistics: {get_kg_statistics(kg)}")
            return True, kg, output_file
    
    return False, kg, None

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Build knowledge graph from PubMed XML')
    parser.add_argument('pubmed_id', type=str, help='PubMed ID')
    parser.add_argument('--output-dir', type=str, default=None, help='Output directory')
    parser.add_argument('--kg-file', type=str, default=None, help='Existing knowledge graph file to update')
    
    args = parser.parse_args()
    
    process_pubmed_xml(args.pubmed_id, args.output_dir, args.kg_file)

if __name__ == "__main__":
    main()
