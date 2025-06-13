"""Test suite for the Knowledge Graph Builder module."""

import os
import unittest

from data_preparation.pubmed_xml_downloader import download_pubmed_xml
from data_preparation.pubmed_xml_parser import parse_pubmed_xml
from knowledge_augmentation.kg_builder import (
    build_knowledge_graph_from_parsed_xml,
    get_kg_statistics,
)


class TestKGBuilder(unittest.TestCase):
    """Unit tests validating KG construction, mutual indexing, and serialization."""

    def setUp(self):
        """Prepare a parsed PubMed XML document for testing."""
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(self.test_dir, exist_ok=True)

        # Example PubMed ID with open-access full-text XML available.
        self.test_pmid = "32133153"
        self.xml_path = os.path.join(self.test_dir, f"pubmed_{self.test_pmid}.xml")

        if not os.path.exists(self.xml_path):
            downloaded = download_pubmed_xml(self.test_pmid, self.test_dir)
            if downloaded:
                self.xml_path = downloaded
            else:
                self.skipTest("Unable to download XML for KG Builder tests.")

        self.parsed = parse_pubmed_xml(self.xml_path)

    def test_build_knowledge_graph(self):
        """Verify that a KG is built with nodes, edges, and mutual indexing."""
        kg, entities_info, relations_info = build_knowledge_graph_from_parsed_xml(
            self.parsed, self.test_pmid
        )

        stats = get_kg_statistics(kg)

        # Ensure nodes and at least one entity were added
        self.assertGreater(stats["node_count"], 0)

        # Mutual indexing: at least one node should contain a non-empty sources list
        found_source = False
        for _, node_data in kg.nodes(data=True):
            if node_data.get("sources"):
                found_source = True
                break
        self.assertTrue(found_source, "No mutual indexing sources found in KG nodes.")

        # Verify serialization round-trip
        save_path = os.path.join(self.test_dir, "temp_kg.json")
        from knowledge_augmentation.kg_builder import save_knowledge_graph, load_knowledge_graph

        self.assertTrue(save_knowledge_graph(kg, save_path))
        kg_loaded = load_knowledge_graph(save_path)
        self.assertIsNotNone(kg_loaded)
        self.assertEqual(kg_loaded.number_of_nodes(), kg.number_of_nodes())
        self.assertEqual(kg_loaded.number_of_edges(), kg.number_of_edges())


if __name__ == "__main__":
    unittest.main()
