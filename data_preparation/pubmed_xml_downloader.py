"""
PubMed XML Downloader

This module provides functionality to download PubMed XML data.
"""

import os
import requests
import time


def construct_pubmed_xml_url(pubmed_id):
    """
    Construct the URL to download PubMed XML for a specific PMID.
    
    Args:
        pubmed_id (str): The PubMed ID (PMID) of the article to download.
        
    Returns:
        str: The URL for downloading the XML.
    """
    # Base URL for PubMed Central open access articles
    base_url = "https://www.ncbi.nlm.nih.gov/research/baylor-covid19/articles/pmc"
    
    # Construct the full URL with the PubMed ID
    url = f"{base_url}/{pubmed_id}/xml/"
    
    return url


def download_pubmed_xml(pubmed_id=None, output_path="."):
    """
    Download PubMed XML data for a given PubMed ID.
    
    Args:
        pubmed_id (str, optional): The PubMed ID (PMID) of the article to download.
            If None, a default example PMID will be used.
        output_path (str, optional): Directory path to save the downloaded XML. 
            Defaults to current directory.
            
    Returns:
        str: The full path to the saved XML file or None if download failed.
    """
    # Use default example PMID if none provided
    if pubmed_id is None:
        # Using a COVID-19 related article as an example
        pubmed_id = "32133153"  # COVID-19 article from 2020
    
    try:
        # Construct URL for downloading
        url = construct_pubmed_xml_url(pubmed_id)
        
        # Make HTTP request to fetch the XML
        print(f"Downloading PubMed XML for PMID: {pubmed_id}")
        response = requests.get(url, timeout=30)
        
        # Check if request was successful
        if response.status_code == 200:
            # Ensure the output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Generate filename based on PMID
            output_file = os.path.join(output_path, f"pubmed_{pubmed_id}.xml")
            
            # Save the XML content to file
            with open(output_file, "wb") as file:
                file.write(response.content)
            
            print(f"Successfully downloaded XML to: {output_file}")
            return output_file
        else:
            print(f"Failed to download XML. Status code: {response.status_code}")
            # Try alternative URL if the first one failed
            return download_from_pubmed_central(pubmed_id, output_path)
    
    except Exception as e:
        print(f"Error downloading PubMed XML: {e}")
        # Try alternative method if the first one failed
        return download_from_pubmed_central(pubmed_id, output_path)


def download_from_pubmed_central(pubmed_id, output_path="."):
    """
    Alternative method to download from PubMed Central directly.
    
    Args:
        pubmed_id (str): The PubMed ID (PMID) of the article to download.
        output_path (str, optional): Directory path to save the downloaded XML.
            
    Returns:
        str: The full path to the saved XML file or None if download failed.
    """
    try:
        # Alternative URL for PMC (PubMed Central)
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
        
        print(f"Trying alternative download method for PMID: {pubmed_id}")
        response = requests.get(url, timeout=30)
        
        # Check if request was successful
        if response.status_code == 200:
            # Ensure the output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Generate filename based on PMID
            output_file = os.path.join(output_path, f"pubmed_{pubmed_id}.xml")
            
            # Save the XML content to file
            with open(output_file, "wb") as file:
                file.write(response.content)
            
            print(f"Successfully downloaded XML to: {output_file}")
            return output_file
        else:
            print(f"Failed to download XML using alternative method. Status code: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Error in alternative download method: {e}")
        return None


def is_valid_pubmed_id(pubmed_id):
    """
    Check if a given string is a valid PubMed ID format.
    
    Args:
        pubmed_id (str): The string to check.
        
    Returns:
        bool: True if the string appears to be a valid PMID, False otherwise.
    """
    if pubmed_id is None:
        return False
        
    # Simple check if the ID contains only digits
    return pubmed_id.isdigit()
