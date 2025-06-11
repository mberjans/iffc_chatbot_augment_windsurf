"""
Test script for PubMed XML Parser
"""

import os
import unittest
from pubmed_xml_parser import parse_pubmed_xml, extract_metadata, extract_abstract
from pubmed_xml_downloader import download_pubmed_xml


class TestPubMedXMLParser(unittest.TestCase):
    """Test cases for PubMed XML parser functions."""

    def setUp(self):
        """Set up test environment."""
        self.test_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Download a test XML file if needed
        self.test_pmid = "32133153"  # COVID-19 article from 2020
        self.test_xml_path = os.path.join(self.test_output_dir, f"pubmed_{self.test_pmid}.xml")
        
        if not os.path.exists(self.test_xml_path):
            self.test_xml_path = download_pubmed_xml(self.test_pmid, self.test_output_dir)
            if not self.test_xml_path:
                self.skipTest("Could not download test XML file")

    def test_parse_pubmed_xml(self):
        """Test the main parsing function."""
        parsed_data = parse_pubmed_xml(self.test_xml_path)
        
        # Check that all sections exist in result
        self.assertIn("metadata", parsed_data)
        self.assertIn("full_text", parsed_data)
        self.assertIn("sections", parsed_data)
        self.assertIn("abstract", parsed_data)
        
        # Check that metadata contains key fields
        metadata = parsed_data["metadata"]
        self.assertIn("pmid", metadata)
        self.assertEqual(metadata["pmid"], self.test_pmid)
        
        # Check that we got some content
        self.assertGreater(len(parsed_data["abstract"]), 0)
        
        # Display some results for manual verification
        print("\nParsed XML test results:")
        print(f"Title: {metadata.get('title', 'N/A')}")
        print(f"Authors: {', '.join(metadata.get('authors', ['N/A']))}")
        print(f"Journal: {metadata.get('journal', 'N/A')}")
        print(f"Publication Date: {metadata.get('pub_date', 'N/A')}")
        print(f"Abstract length: {len(parsed_data['abstract'])} characters")
        print(f"Full text length: {len(parsed_data['full_text'])} characters")
        print(f"Sections found: {len(parsed_data['sections'])}")
        
    def test_extract_metadata(self):
        """Test metadata extraction function."""
        from lxml import etree
        
        # Create a simple XML tree for testing
        xml_content = """
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345</PMID>
                <Article>
                    <ArticleTitle>Test Article Title</ArticleTitle>
                    <Journal>
                        <Title>Test Journal</Title>
                    </Journal>
                    <AuthorList>
                        <Author>
                            <LastName>Smith</LastName>
                            <ForeName>John</ForeName>
                        </Author>
                        <Author>
                            <LastName>Doe</LastName>
                            <ForeName>Jane</ForeName>
                        </Author>
                    </AuthorList>
                </Article>
                <KeywordList>
                    <Keyword>Test</Keyword>
                    <Keyword>XML</Keyword>
                </KeywordList>
            </MedlineCitation>
            <PubmedData>
                <ArticleIdList>
                    <ArticleId IdType="doi">10.1234/test</ArticleId>
                </ArticleIdList>
            </PubmedData>
        </PubmedArticle>
        """
        
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(xml_content, parser).getroottree()
        
        # Extract metadata and verify results
        metadata = extract_metadata(tree)
        
        self.assertEqual(metadata["pmid"], "12345")
        self.assertEqual(metadata["doi"], "10.1234/test")
        self.assertEqual(metadata["title"], "Test Article Title")
        self.assertEqual(metadata["journal"], "Test Journal")
        self.assertEqual(len(metadata["authors"]), 2)
        self.assertIn("John Smith", metadata["authors"])
        self.assertIn("Jane Doe", metadata["authors"])
        self.assertEqual(len(metadata["keywords"]), 2)
        self.assertIn("Test", metadata["keywords"])
        self.assertIn("XML", metadata["keywords"])


if __name__ == "__main__":
    unittest.main()
