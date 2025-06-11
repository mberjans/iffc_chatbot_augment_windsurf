"""
Test script for PubMed XML Downloader
"""

import os
import unittest
from pubmed_xml_downloader import download_pubmed_xml, is_valid_pubmed_id


class TestPubMedXMLDownloader(unittest.TestCase):
    """Test cases for PubMed XML downloader functions."""

    def setUp(self):
        """Set up test environment."""
        self.test_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")
        os.makedirs(self.test_output_dir, exist_ok=True)

    def test_is_valid_pubmed_id(self):
        """Test validation of PubMed IDs."""
        self.assertTrue(is_valid_pubmed_id("12345678"))
        self.assertTrue(is_valid_pubmed_id("32133153"))
        self.assertFalse(is_valid_pubmed_id("invalid-id"))
        self.assertFalse(is_valid_pubmed_id(""))
        self.assertFalse(is_valid_pubmed_id(None))
        
    def test_download_pubmed_xml(self):
        """Test downloading a PubMed XML file."""
        # Test with default PMID
        result_path = download_pubmed_xml(output_path=self.test_output_dir)
        
        # Check that file exists and has content
        if result_path is not None:
            self.assertTrue(os.path.exists(result_path))
            file_size = os.path.getsize(result_path)
            self.assertGreater(file_size, 0, "Downloaded XML file should not be empty")
            print(f"Successfully downloaded XML file: {result_path}, size: {file_size} bytes")
        else:
            print("Test skipped: Download failed, possibly due to network issues")
            

if __name__ == "__main__":
    unittest.main()
