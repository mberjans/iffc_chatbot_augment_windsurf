"""
PubMed XML Parser Utility

This module provides functions for parsing PubMed XML files to extract
metadata, full text content, and article sections.
"""

import os
from lxml import etree
import re


def load_xml_from_file(xml_file_path):
    """
    Load and parse an XML file into an lxml ElementTree.
    
    Args:
        xml_file_path (str): Path to the XML file to parse
        
    Returns:
        etree._ElementTree: The parsed XML tree, or None if parsing failed
    """
    if not os.path.exists(xml_file_path):
        print(f"Error: File {xml_file_path} does not exist.")
        return None
        
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file_path, parser)
        return tree
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return None


def extract_metadata(xml_tree):
    """
    Extract key metadata from a PubMed XML document.
    
    Args:
        xml_tree (etree._ElementTree): Parsed XML tree
        
    Returns:
        dict: Dictionary containing metadata fields including:
            - pmid: PubMed ID
            - doi: Digital Object Identifier
            - title: Article title
            - journal: Journal name
            - pub_date: Publication date
            - authors: List of authors
            - keywords: List of keywords
    """
    if xml_tree is None:
        return {}
    
    root = xml_tree.getroot()
    metadata = {}
    
    # Extract PMID
    pmid_elements = root.xpath(".//PMID")
    if pmid_elements:
        metadata["pmid"] = pmid_elements[0].text.strip()
    
    # Extract DOI
    doi_elements = root.xpath(".//ArticleId[@IdType='doi']")
    if doi_elements:
        metadata["doi"] = doi_elements[0].text.strip()
    
    # Extract title
    title_elements = root.xpath(".//ArticleTitle")
    if title_elements:
        metadata["title"] = "".join(title_elements[0].xpath(".//text()"))
    
    # Extract journal information
    journal_elements = root.xpath(".//Journal/Title")
    if journal_elements:
        metadata["journal"] = journal_elements[0].text.strip()
    
    # Extract publication date
    year_elements = root.xpath(".//PubDate/Year")
    month_elements = root.xpath(".//PubDate/Month")
    day_elements = root.xpath(".//PubDate/Day")
    
    pub_date = ""
    if year_elements:
        pub_date = year_elements[0].text.strip()
        if month_elements:
            pub_date = month_elements[0].text.strip() + " " + pub_date
            if day_elements:
                pub_date = day_elements[0].text.strip() + " " + pub_date
    
    metadata["pub_date"] = pub_date
    
    # Extract authors
    author_elements = root.xpath(".//Author")
    authors = []
    
    for author_elem in author_elements:
        last_name = author_elem.xpath("./LastName/text()")
        first_name = author_elem.xpath("./ForeName/text()") or author_elem.xpath("./FirstName/text()")
        
        author_name = ""
        if last_name:
            author_name = last_name[0].strip()
        if first_name:
            if author_name:
                author_name = first_name[0].strip() + " " + author_name
            else:
                author_name = first_name[0].strip()
        
        if author_name:
            authors.append(author_name)
    
    metadata["authors"] = authors
    
    # Extract keywords
    keyword_elements = root.xpath(".//Keyword")
    keywords = []
    
    for keyword_elem in keyword_elements:
        keyword_text = keyword_elem.text
        if keyword_text:
            keywords.append(keyword_text.strip())
    
    metadata["keywords"] = keywords
    
    return metadata


def extract_abstract(xml_tree):
    """
    Extract the abstract from a PubMed XML document.
    
    Args:
        xml_tree (etree._ElementTree): Parsed XML tree
        
    Returns:
        str: The abstract text
    """
    if xml_tree is None:
        return ""
    
    root = xml_tree.getroot()
    
    # Try to get structured abstract sections first
    abstract_sections = root.xpath(".//AbstractText")
    if abstract_sections:
        abstract_parts = []
        
        for section in abstract_sections:
            section_label = section.get("Label", "")
            section_text = "".join(section.xpath(".//text()")) if section.text is None else section.text
            
            if section_label:
                abstract_parts.append(f"{section_label}: {section_text}")
            else:
                abstract_parts.append(section_text)
        
        return "\n\n".join(abstract_parts)
    
    # Fall back to simple abstract extraction
    abstract_elements = root.xpath(".//Abstract")
    if abstract_elements:
        return "".join(abstract_elements[0].xpath(".//text()"))
    
    # Try other common locations for abstract text
    article_summary = root.xpath(".//ArticleSummary/text()") or root.xpath(".//Summary/text()")
    if article_summary:
        return "\n".join([summary.strip() for summary in article_summary])
    
    # Check if abstract might be in a different location
    article_elements = root.xpath(".//Article")
    if article_elements:
        for article in article_elements:
            # Look for any element that might contain abstract text
            for elem_name in ["Abstract", "ArticleSummary", "Summary", "Description"]:
                elements = article.xpath(f".//{elem_name}")
                if elements:
                    text = "".join(elements[0].xpath(".//text()"))
                    if text.strip():
                        return text.strip()
    
    # As a last resort, try to get any text that might be descriptive from the article title
    title_elements = root.xpath(".//ArticleTitle")
    if title_elements:
        return f"[No abstract available. Article title: {title_elements[0].text}]"
    
    return "[No abstract available]"


def extract_full_text(xml_tree):
    """
    Extract the full text content from a PubMed XML document.
    
    Args:
        xml_tree (etree._ElementTree): Parsed XML tree
        
    Returns:
        str: The full text content of the article
    """
    if xml_tree is None:
        return ""
    
    root = xml_tree.getroot()
    
    # Look for full text in body
    body_elements = root.xpath(".//body")
    if body_elements:
        return "".join(body_elements[0].xpath(".//text()"))
    
    # If no body element is found, combine abstract and other sections
    text_parts = []
    
    # Add abstract
    abstract = extract_abstract(xml_tree)
    if abstract:
        text_parts.append(abstract)
    
    # Add any other text content
    article_elements = root.xpath(".//Article")
    if article_elements:
        for article in article_elements:
            # Skip elements that were already included in the abstract
            for element in article.xpath(".//*[not(ancestor::Abstract)]"):
                if element.text and element.text.strip():
                    text_parts.append(element.text.strip())
    
    return "\n\n".join(text_parts)


def clean_text(text):
    """
    Clean and normalize text content.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove HTML-like tags
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()


def extract_sections(xml_tree):
    """
    Extract distinct sections from a PubMed XML document.
    
    Args:
        xml_tree (etree._ElementTree): Parsed XML tree
        
    Returns:
        dict: Dictionary with section names as keys and section content as values
    """
    if xml_tree is None:
        return {}
    
    root = xml_tree.getroot()
    sections = {}
    
    # Extract abstract as a section
    abstract = extract_abstract(xml_tree)
    if abstract:
        sections["abstract"] = abstract
    
    # Extract common PMC article sections
    section_elements = root.xpath(".//sec")
    
    for section in section_elements:
        # Get section title
        title_element = section.xpath("./title")
        if title_element:
            section_title = title_element[0].text.strip().lower()
            if not section_title:
                section_title = "section_" + str(len(sections))
        else:
            section_title = "section_" + str(len(sections))
        
        # Get section content
        section_text = "".join(section.xpath(".//text()"))
        section_text = clean_text(section_text)
        
        # Avoid duplicate section titles
        if section_title in sections:
            section_title = section_title + "_" + str(len(sections))
        
        sections[section_title] = section_text
    
    # If no sections found, check for more generic divisions
    if len(sections) <= 1:  # Only abstract was found
        div_elements = root.xpath(".//div")
        
        for i, div in enumerate(div_elements):
            div_title = f"section_{i + 1}"
            
            # Try to extract a title
            title_element = div.xpath("./title") or div.xpath(".//h1") or div.xpath(".//h2")
            if title_element:
                div_title = title_element[0].text.strip().lower()
            
            div_text = "".join(div.xpath(".//text()"))
            div_text = clean_text(div_text)
            
            if div_text and (div_title not in sections):
                sections[div_title] = div_text
    
    return sections


def parse_pubmed_xml(xml_file_path):
    """
    Main function to parse a PubMed XML file and extract structured data.
    
    Args:
        xml_file_path (str): Path to the XML file to parse
        
    Returns:
        dict: Dictionary containing all parsed data including:
            - metadata: Dictionary of article metadata
            - full_text: Complete article text
            - sections: Dictionary of article sections
            - abstract: Article abstract
    """
    xml_tree = load_xml_from_file(xml_file_path)
    if xml_tree is None:
        return {
            "metadata": {},
            "full_text": "",
            "sections": {},
            "abstract": ""
        }
    
    # Extract all components
    metadata = extract_metadata(xml_tree)
    abstract = extract_abstract(xml_tree)
    full_text = extract_full_text(xml_tree)
    sections = extract_sections(xml_tree)
    
    # Return structured data
    return {
        "metadata": metadata,
        "full_text": full_text,
        "sections": sections,
        "abstract": abstract
    }
