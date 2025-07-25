# Nexus Scholar AI - Implementation Progress

This document tracks the implementation progress of the Nexus Scholar AI project.

## Foundational Setup (Agent: DATA_PREP)

### Ticket ID: NXS-0Z-001 - Create PubMed XML Downloader/Fetcher

Completed on: June 10, 2025

Implemented functions:
- `download_pubmed_xml(pubmed_id=None, output_path=".")`: Main function to download PubMed XML by PubMed ID
- `construct_pubmed_xml_url(pubmed_id)`: Helper to build the primary download URL
- `download_from_pubmed_central(pubmed_id, output_path=".")`: Alternative download method using NCBI eUtils API
- `is_valid_pubmed_id(pubmed_id)`: Simple validation function for PubMed IDs

Features:
- Downloads PubMed XML documents using direct URL or eUtils API
- Falls back to alternative download method when primary fails
- Validates PubMed IDs
- Handles network errors gracefully
- Saves XML files with consistent naming convention

### Ticket ID: NXS-1Z-001: PubMed XML Parser Utility

Completed on: June 11, 2025

Implemented functions:
- `parse_pubmed_xml(xml_file_path)`: Main function to parse a PubMed XML file and extract structured data
- `load_xml_from_file(xml_file_path)`: Load and parse an XML file into an lxml ElementTree
- `extract_metadata(xml_tree)`: Extract key metadata (PMID, DOI, title, journal info, authors, etc.)
- `extract_abstract(xml_tree)`: Extract abstract text with fallbacks for different XML structures
- `extract_full_text(xml_tree)`: Extract the full text content from a PubMed XML document
- `extract_sections(xml_tree)`: Extract distinct sections from a PubMed XML document
- `clean_text(text)`: Helper function to clean and normalize text content

Features:
- Comprehensive metadata extraction including authors, publication dates, journal info
- Robust abstract extraction with multiple fallback approaches for different XML formats
- Full-text extraction from PubMed XML
- Section identification and extraction
- Text normalization and cleaning
- Error handling for malformed or missing XML

## Knowledge Augmentation Development (Agent: KAG_DEV)

### Ticket ID: NXS-1A-001 - Implement KAG-Builder: XML to Knowledge Graph

#### Task: KAG_DEV-NXS-1A-001-DEFINE_KG_SCHEMA

Completed on: June 11, 2025

Implemented in `kg_schema.py`:

**Entity Types:**
Enhanced the biomedical knowledge graph schema with comprehensive entity types including:
- Basic entities: DRUG, DISEASE, GENE, PROTEIN, PATHWAY
- Clinical entities: SYMPTOM, ANATOMY, CLINICAL_FEATURE
- Biological entities: ORGANISM, CELL_TYPE, METABOLITE
- Process entities: BIOLOGICAL_PROCESS, METHOD
- Chemical entities: CHEMICAL

Each entity type includes:
- Description: Detailed explanation of the entity type
- Examples: Representative samples to guide entity extraction

**Relation Types:**
Implemented a comprehensive set of relationship types including:
- Treatment relationships: TREATS
- Causal relationships: CAUSES, ACTIVATES, INHIBITS
- Associative relationships: ASSOCIATED_WITH, INTERACTS_WITH, COOCCURS_WITH
- Structural relationships: PART_OF
- Biological relationships: EXPRESSED_IN, CONVERTS_TO, BIOMARKER_FOR, REGULATES, METABOLIZED_BY, USED_IN

Each relation type includes:
- Description: Detailed explanation of the relationship
- Subject/object type constraints: Lists of valid entity types for each position
- Examples: Representative triplets to guide relation extraction

**Utility Functions:**
Implemented schema validation and query functions:
- `get_all_entity_types()`: Get list of all entity type names
- `get_all_relation_types()`: Get list of all relation type names
- `get_entity_description()`: Get description for a specific entity type
- `get_relation_description()`: Get description for a specific relation type
- `is_valid_entity_type()`: Check if an entity type is valid in the schema
- `is_valid_relation()`: Validate if a relation triplet conforms to schema constraints
- `get_valid_relation_types_between()`: Find valid relationships between two entity types
- `get_entity_examples()`: Get examples for an entity type
- `get_relation_example()`: Get an example for a relation type
- `get_relation_subject_types()`: Get valid subject types for a relation
- `get_relation_object_types()`: Get valid object types for a relation

The schema is designed to support the Knowledge Augmented Generation (KAG) pattern with mutual indexing between the knowledge graph and source text for accurate citation generation.

#### Task: KAG_DEV-NXS-1A-001-CHOOSE_KG_LIBRARY

Completed on: June 11, 2025

Selected NetworkX as the knowledge graph library for the KAG module implementation.

**Key features that led to choosing NetworkX:**
- **Graph Types**: Supports multiple graph types including directed graphs and multigraphs (MultiDiGraph), which are essential for representing complex biomedical relationships where multiple edges can exist between the same nodes.
- **Python Integration**: Seamlessly integrates with other Python libraries and offers a Pythonic API.
- **Serialization**: Provides built-in methods for graph serialization with `node_link_data()` and deserialization with `node_link_graph()`, facilitating easy saving/loading of knowledge graphs.
- **Traversal Algorithms**: Rich set of graph algorithms for path finding, centrality measures, and community detection.
- **Lightweight**: In-memory graph representation that's efficient for the project's requirements.
- **Extensibility**: Allows custom node and edge attributes which is critical for storing entity types, relations, and mutual indexing references.

**Implementation in `kg_builder.py`:**
- Used MultiDiGraph for the knowledge graph implementation to support multiple relationship types between entities
- Implemented graph creation, node/edge addition, and serialization methods
- Provided utility functions for graph traversal and querying

#### Task: KAG_DEV-NXS-1A-001-SETUP_NER_TOOL

Completed on: June 11, 2025

Implemented in `ner_extractor.py`:

Set up spaCy with biomedical models for named entity recognition in biomedical texts.

**Core Functions:**
- `download_biomedical_model()`: Downloads the biomedical NER model for spaCy if not already available, with multiple fallback methods.
- `setup_spacy_model()`: Sets up and returns the spaCy model for biomedical NER, with fallbacks to simpler models if needed.
- `map_ner_to_schema()`: Maps NER entity types from spaCy to our custom schema entity types.
- `extract_entities_with_ner()`: Extracts entities from text using spaCy NER, returning a list with type, text, and position information.
- `extract_entities_from_sections_with_ner()`: Processes multiple document sections using NER.
- `extract_entities_from_parsed_xml_with_ner()`: Extracts entities from parsed PubMed XML data structure.
- `merge_entity_extractions()`: Merges entities from rule-based and NER approaches, handling duplicates.

**Technical Details:**
- Uses `en_core_sci_md` as the primary biomedical model
- Implements entity type mapping between spaCy's biomedical entities and our custom schema
- Handles model download and installation if not available
- Provides fallback mechanisms to simpler models when necessary
- Extracts entity metadata including normalized text, position, and type

**Schema Integration:**
- Maps extracted entities to our defined schema entity types
- DEFAULT_ENTITY_MAPPING provides the connection between spaCy entity labels and our schema
- Integration with the knowledge graph schema for consistent entity typing

#### Task: KAG_DEV-NXS-1A-001-IMPLEMENT_ENTITY_EXTRACTION

Completed on: June 11, 2025

Implemented in `entity_extractor.py`:

Created a comprehensive entity extraction module that combines multiple extraction approaches to identify biomedical entities in PubMed XML data.

**Core Functions:**
- `load_entity_dictionary()`: Loads entity dictionaries from disk for dictionary-based extraction
- `normalize_entity_text()`: Normalizes entity text for consistent matching and deduplication
- `extract_entities_with_dictionary()`: Extracts entities using dictionary-based pattern matching
- `extract_entities_with_rule_based()`: Orchestrates rule-based entity extraction across multiple entity types
- `extract_entities_from_parsed_xml()`: Main function that combines NER and rule-based approaches
- `get_entity_statistics()`: Generates statistics about extracted entities
- `merge_duplicate_entities()`: Deduplicates extracted entities based on normalized text and type

**Key Features:**
- Hybrid extraction approach combining NER and dictionary-based methods
- Non-regex pattern matching as per project requirements
- Entity normalization for consistent identification
- Entity validation against the schema
- Automatic deduplication of entities from different extraction methods
- Section-aware extraction that preserves source context
- Support for extracting entities from abstract, full text, or specific sections

**Integration Points:**
- Uses the NER extractor module for ML-based entity recognition
- Validates extracted entities against the knowledge graph schema
- Prepares entities in a format suitable for knowledge graph construction
- Maintains entity positions within text for mutual indexing support

#### Task: KAG_DEV-NXS-1A-001-IMPLEMENT_RELATION_EXTRACTION

Completed on: June 12, 2025

Implemented in `knowledge_augmentation/entity_extraction.py`:

Added functionality to extract relationships between entities based on co-occurrence within the same sentence. This is a foundational step for building the knowledge graph.

**Core Functions:**
- `extract_relationships_cooccurrence(text_segment_normalized: str, entities_in_segment: list) -> list`: Identifies pairs of entities that appear in the same sentence within a given normalized text segment. Entity positions must be relative to this segment. Returns a list of relationship objects, each detailing the two entities, their types, positions, the relationship type ('co-occurs_in_sentence'), and the normalized sentence context.
- `extract_relationships_from_parsed_xml(parsed_xml_data: dict, extracted_entities_info: dict) -> dict`: Orchestrates relation extraction across different parts of a parsed XML document (e.g., abstract, sections). It uses `extract_relationships_cooccurrence` for each text part, leveraging the previously extracted entities and their positions. Returns a dictionary of relationships categorized by their source context (e.g., 'abstract', 'section_name').

**Key Features:**
- Sentence-level co-occurrence: Relationships are established if entities are found within the same sentence.
- Context preservation: The normalized sentence in which co-occurrence is found is stored with the relationship.
- Integration with existing entity extraction: Uses entity information (text, type, position) generated by prior extraction steps.
- XML structure awareness: Processes abstract and various text sections from parsed XML data.
- Normalization consistency: Ensures that text normalization applied during relation extraction matches that used for entity extraction, critical for accurate position mapping.


## Ticket 1: Data Ingestion

### Task 1.1: Create a function to download data from a specified URL.
- **Function:** `download_data(url, save_path)`
- **Module:** `data_ingestion/downloader.py`
- **Status:** Completed
- **Notes:** Downloads data from a URL and saves it locally. Includes basic error handling and directory creation if needed. A test case is provided in the `if __name__ == '__main__':` block, which requires a local HTTP server for testing.
