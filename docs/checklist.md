**Foundational Setup (Agent: DATA_PREP)**

**Ticket ID:** DI-UTIL-001

* **Title:** General Data Download Utility
* **Checklist:**
  * [x] DI-UTIL-001-CREATE_DOWNLOAD_FUNCTION: Create a generic function `download_data(url, save_path)` to download data from a URL.

**Ticket ID:** NXS-0Z-001

* **Title:** Create PubMed XML Downloader/Fetcher  
* **Checklist:**  
  * \[x\] DATA_PREP-NXS-0Z-001-RESEARCH_LIBRARIES: Research Python libraries for HTTP requests (e.g., requests) or specialized PubMed access (e.g., BioPython, pubmedparser2 1).  
  * \[x\] DATA_PREP-NXS-0Z-001-DEFINE_FUNCTION_SIGNATURE: Define the Python function signature (e.g., download_pubmed_xml(pubmed_id=None, output_path=".")).  
  * \[x\] DATA_PREP-NXS-0Z-001-IMPLEMENT_DOWNLOAD_LOGIC: Implement logic to construct the download URL for a given PubMed ID or a default example.  
  * \[x\] DATA_PREP-NXS-0Z-001-HANDLE_REQUEST_EXECUTION: Implement the HTTP GET request to fetch the XML data.  
  * \[x\] DATA_PREP-NXS-0Z-001-ERROR_HANDLING: Add error handling for network issues or invalid PubMed IDs.  
  * \[x\] DATA_PREP-NXS-0Z-001-SAVE_TO_FILE: Implement logic to save the downloaded XML content to a specified local file path.  
  * \[x\] DATA_PREP-NXS-0Z-001-ADD_DOCSTRINGS_COMMENTS: Add docstrings and comments to the script.  
  * \[x\] DATA_PREP-NXS-0Z-001-UNIT_TEST_DOWNLOAD: Write a unit test to verify successful download and file creation.

**Ticket ID:** NXS-1Z-001

* **Title:** Develop Core PubMed XML Parser Utility  
* **Checklist:**  
  * \[x\] DATA\_PREP-NXS-1Z-001-CHOOSE\_PARSING\_LIBRARY: Decide on XML parsing library (recommend pubmedparser2 1 or lxml).  
  * \[x\] DATA\_PREP-NXS-1Z-001-DEFINE\_PARSER\_CLASS: Define PubMedXMLParser class structure.  
  * \[x\] DATA\_PREP-NXS-1Z-001-IMPLEMENT\_INITIALIZATION: Implement \_\_init\_\_ method to take XML file path.  
  * \[x\] DATA\_PREP-NXS-1Z-001-DEFINE\_EXTRACTION\_SCHEMA: If using pubmedparser2, define the YAML or dictionary structure for desired elements (full text, sections, metadata).1  
  * \[x\] DATA\_PREP-NXS-1Z-001-IMPLEMENT\_METADATA\_EXTRACTION: Implement method to parse and extract key metadata (PMID, title, authors, journal, date, keywords).  
  * \[x\] DATA\_PREP-NXS-1Z-001-IMPLEMENT\_FULL\_TEXT\_EXTRACTION: Implement method to parse and extract the clean full text.  
  * \[x\] DATA\_PREP-NXS-1Z-001-IMPLEMENT\_SECTION\_EXTRACTION: Implement method to parse and extract distinct sections (abstract, methods, results, etc.), preserving their identity.  
  * \[x\] DATA\_PREP-NXS-1Z-001-STRUCTURE\_OUTPUT: Define the output format (e.g., a dictionary or custom data objects) for the parsed data.  
  * \[x\] DATA\_PREP-NXS-1Z-001-ERROR\_HANDLING: Add error handling for malformed XML or missing expected elements.  
  * \[x\] DATA\_PREP-NXS-1Z-001-ADD\_DOCSTRINGS\_COMMENTS: Add comprehensive docstrings and comments.  
  * \[x\] DATA\_PREP-NXS-1Z-001-UNIT\_TEST\_PARSING: Write unit tests using the example XML from NXS-0Z-001 to verify correct extraction of all defined fields.

---

**Phase 1: Develop Independent Answering Modules**

**Agent: KAG\_DEV (Knowledge Augmented Generation Module)**

**Ticket ID:** NXS-1A-001

* **Title:** Implement KAG-Builder: XML to Knowledge Graph  
* **Checklist:**  
  * [x] KAG_DEV-NXS-1A-001-DEFINE_KG_SCHEMA: Define a preliminary schema for the biomedical KG (entities: e.g., medical terms, genes; relationships: e.g., treats, causes).  
  * [x] KAG_DEV-NXS-1A-001-CHOOSE_KG_LIBRARY: Select KG library (e.g., NetworkX).  
  * [x] KAG_DEV-NXS-1A-001-SETUP_NER_TOOL: Set up NER tool (e.g., spaCy with en_core_sci_sm or LLM-based NER).  
  * [x] KAG_DEV-NXS-1A-001-IMPLEMENT_ENTITY_EXTRACTION: Implement function to extract entities from parsed text (from NXS-1Z-001) based on the schema.  
  * [x] KAG_DEV-NXS-1A-001-IMPLEMENT_RELATION_EXTRACTION: Implement function to extract relationships between identified entities (e.g., co-occurrence, rule-based, or LLM-based).  
  * [x] KAG_DEV-NXS-1A-001-IMPLEMENT_KG_CONSTRUCTION: Implement function to populate the chosen KG library with extracted entities and relations.  
  * [x] KAG_DEV-NXS-1A-001-IMPLEMENT_MUTUAL_INDEXING: Design and implement data structure to link KG nodes/edges back to specific text chunks/sections from the source XML (critical for citations).2  
  * [x] KAG_DEV-NXS-1A-001-SERIALIZE_KG_INDEX: Implement logic to save/load the KG and mutual index if on-disk persistence is chosen.  
  * [x] KAG_DEV-NXS-1A-001-UNIT_TEST_KG_BUILDER: Write unit tests for entity extraction, relation extraction, and KG construction using parsed XML.

**Ticket ID:** NXS-1A-002

* **Title:** Implement KAG-Solver/Model: KG Querying and Answer Synthesis  
* **Checklist:**  
  * \[ \] KAG\_DEV-NXS-1A-002-DEFINE\_MODULE\_CLASS: Define the main KAG answering module class.  
  * \[ \] KAG\_DEV-NXS-1A-002-IMPLEMENT\_KG\_LOADING: Implement logic to load the KG and mutual index (from NXS-1A-001).  
  * \[ \] KAG\_DEV-NXS-1A-002-DEVELOP\_KG\_QUERY\_STRATEGY: Design strategy to identify relevant entry nodes/subgraphs in the KG based on user question keywords.  
  * \[ \] KAG\_DEV-NXS-1A-002-IMPLEMENT\_KG\_TRAVERSAL: Implement KG traversal/query execution logic.  
  * \[ \] KAG\_DEV-NXS-1A-002-FORMAT\_CONTEXT\_FOR\_LLM: Implement function to format retrieved KG context for LLM input.  
  * \[ \] KAG\_DEV-NXS-1A-002-INTEGRATE\_LLM\_API: Integrate with an LLM API for answer synthesis.  
  * \[ \] KAG\_DEV-NXS-1A-002-PROMPT\_ENGINEERING\_SYNTHESIS: Develop prompts for the LLM to synthesize an answer based on KG context.  
  * \[ \] KAG\_DEV-NXS-1A-002-IMPLEMENT\_CITATION\_GENERATION: Implement logic to generate citations using the mutual indexing data and original XML.  
  * \[ \] KAG\_DEV-NXS-1A-002-DEFINE\_OUTPUT\_FORMAT: Define the output format (answer string, list of citation objects).  
  * \[ \] KAG\_DEV-NXS-1A-002-UNIT\_TEST\_KAG\_SOLVER: Write unit tests for the full query-to-answer pipeline.

**Agent: GRAPHRAG\_DEV (GraphRAG Module)**

**Ticket ID:** NXS-1B-001

* **Title:** Implement GraphRAG Indexing Phase: XML to Document Knowledge Graph  
* **Checklist:**  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-CHOOSE\_GRAPH\_LIBRARY: Select graph library (e.g., NetworkX or a library specific to a GraphRAG framework like Microsoft's 3 or Neo4j's 6).  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-IMPLEMENT\_TEXT\_CHUNKING: Implement text chunking strategy for nodes (e.g., paragraphs, sentences from parsed XML).  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-IMPLEMENT\_NODE\_CREATION: Implement logic to create graph nodes from text chunks or extracted entities.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-IMPLEMENT\_EDGE\_CREATION: Implement logic to establish edges (sequential, semantic similarity using embeddings, co-occurrence).  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-OPTIONAL\_COMMUNITY\_DETECTION: (Optional) Research and implement community detection algorithms if pursuing advanced GraphRAG.3  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-OPTIONAL\_COMMUNITY\_SUMMARIES: (Optional) If communities are detected, implement LLM-based summarization for them.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-SERIALIZE\_GRAPH: Implement logic to save/load the graph representation.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-001-UNIT\_TEST\_INDEXING: Write unit tests for graph construction from parsed XML.

**Ticket ID:** NXS-1B-002

* **Title:** Implement GraphRAG Querying Phase: Graph Traversal and Answer Synthesis  
* **Checklist:**  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-DEFINE\_MODULE\_CLASS: Define the main GraphRAG answering module class.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-IMPLEMENT\_GRAPH\_LOADING: Implement logic to load the graph (from NXS-1B-001).  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-IMPLEMENT\_LOCAL\_SEARCH: Implement local search logic (entity-focused graph traversal).3  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-IMPLEMENT\_GLOBAL\_SEARCH: Implement global search logic (thematic queries, possibly using community summaries).3  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-FORMAT\_CONTEXT\_FOR\_LLM: Implement function to format retrieved graph context (nodes, paths) for LLM input.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-INTEGRATE\_LLM\_API: Integrate with an LLM API for answer synthesis.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-PROMPT\_ENGINEERING\_SYNTHESIS: Develop prompts for the LLM.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-IMPLEMENT\_CITATION\_GENERATION: Implement citation generation based on source of graph nodes.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-DEFINE\_OUTPUT\_FORMAT: Define the output format.  
  * \[ \] GRAPHRAG\_DEV-NXS-1B-002-UNIT\_TEST\_QUERYING: Write unit tests for the full query-to-answer pipeline.

**Agent: LIGHTRAG\_DEV (LightRAG Module)**

**Ticket ID:** NXS-1C-001

* **Title:** Implement LightRAG Knowledge Graph and Vector Index Construction  
* **Checklist:**  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-SETUP\_LIGHTRAG\_ENV: Install LightRAG library and dependencies.7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-IMPLEMENT\_TEXT\_CHUNKING: Implement text chunking from parsed XML.  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-IMPLEMENT\_ENTITY\_RELATION\_EXTRACTION: Implement entity and relationship extraction (likely using LightRAG's internal LLM calls).7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-IMPLEMENT\_KG\_CONSTRUCTION: Use LightRAG functions to build its knowledge graph.7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-IMPLEMENT\_EMBEDDING\_STORAGE: Use LightRAG functions to embed entity/relationship descriptions and store them in its vector DB (e.g., nano\_vectordb).7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-CONFIGURE\_LIGHTRAG\_INSTANCE: Configure LightRAG instance with appropriate LLM and embedding models (e.g., HuggingFace models as per 8).  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-001-UNIT\_TEST\_INDEXING: Write unit tests for data ingestion and index creation.

**Ticket ID:** NXS-1C-002

* **Title:** Implement LightRAG Dual-Level Retrieval and Answer Synthesis  
* **Checklist:**  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-DEFINE\_MODULE\_CLASS: Define the main LightRAG answering module class.  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-IMPLEMENT\_KEYWORD\_GENERATION: Use LightRAG's LLM integration to generate keywords from user question.7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-IMPLEMENT\_LOW\_LEVEL\_RETRIEVAL: Implement LightRAG's low-level retrieval for specific entities/attributes.7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-IMPLEMENT\_HIGH\_LEVEL\_RETRIEVAL: Implement LightRAG's high-level retrieval for broader concepts.7  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-INTEGRATE\_LLM\_SYNTHESIS: Use LightRAG's mechanisms to pass retrieved context to an LLM for answer synthesis.  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-IMPLEMENT\_CITATION\_GENERATION: Adapt LightRAG output to include citations if possible (may require mapping back to original XML).  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-DEFINE\_OUTPUT\_FORMAT: Define the output format.  
  * \[ \] LIGHTRAG\_DEV-NXS-1C-002-UNIT\_TEST\_QUERYING: Write unit tests for different query modes (hybrid, naive).7

**Agent: TRADRAG\_DEV (Traditional RAG Module)**

**Ticket ID:** NXS-1D-001

* **Title:** Implement Traditional RAG: Text Processing and Vector Indexing  
* **Checklist:**  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-EXTRACT\_CLEAN\_TEXT: Extract clean text from parsed XML (NXS-1Z-001).  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-IMPLEMENT\_TEXT\_CHUNKING: Implement text chunking strategy (e.g., paragraph, fixed size with overlap).  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-CHOOSE\_EMBEDDING\_MODEL: Select sentence-transformer model (e.g., all-MiniLM-L6-v2).  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-IMPLEMENT\_EMBEDDING\_GENERATION: Implement function to generate embeddings for each chunk.  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-CHOOSE\_VECTOR\_DB: Select vector DB (FAISS for in-memory, ChromaDB for on-disk).  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-IMPLEMENT\_VECTOR\_INDEXING: Implement logic to build and save the vector index with chunks and embeddings.  
  * \[ \] TRADRAG\_DEV-NXS-1D-001-UNIT\_TEST\_INDEXING: Write unit tests for chunking, embedding, and indexing.

**Ticket ID:** NXS-1D-002

* **Title:** Implement Traditional RAG: Query Processing and Answer Synthesis  
* **Checklist:**  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-DEFINE\_MODULE\_CLASS: Define the main Traditional RAG answering module class.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-IMPLEMENT\_INDEX\_LOADING: Implement logic to load the vector index.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-IMPLEMENT\_QUERY\_EMBEDDING: Embed user question using the same sentence-transformer.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-IMPLEMENT\_SIMILARITY\_SEARCH: Implement k-NN similarity search against the vector index.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-FORMAT\_CONTEXT\_FOR\_LLM: Format retrieved chunks for LLM input.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-INTEGRATE\_LLM\_API: Integrate with an LLM API for answer synthesis.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-PROMPT\_ENGINEERING\_SYNTHESIS: Develop prompts for the LLM.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-IMPLEMENT\_CITATION\_GENERATION: Implement citation generation based on source of retrieved chunks (map back to original XML).  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-DEFINE\_OUTPUT\_FORMAT: Define the output format.  
  * \[ \] TRADRAG\_DEV-NXS-1D-002-UNIT\_TEST\_QUERYING: Write unit tests for the full query-to-answer pipeline.

**Agent: WEBSEARCH\_DEV (Web-Search Module \- Perplexity API)**

**Ticket ID:** NXS-1E-001

* **Title:** Implement Perplexity API Integration Wrapper  
* **Checklist:**  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-RESEARCH\_API\_DOCS: Review Perplexity API documentation for endpoints, auth, and models.9  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-DEFINE\_CLIENT\_CLASS: Define PerplexityAPIClient class.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-IMPLEMENT\_INITIALIZATION: \_\_init\_\_ to take API key.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-IMPLEMENT\_BASE\_REQUEST\_FUNCTION: Implement a private method for making generic POST requests to https://api.perplexity.ai/chat/completions.9  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-HANDLE\_AUTHENTICATION: Implement Bearer Token authentication in requests.9  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-HANDLE\_JSON\_RESPONSE\_PARSING: Implement JSON response parsing.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-IMPLEMENT\_ERROR\_HANDLING: Implement error handling for API errors (rate limits, auth failures, etc.).  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-001-UNIT\_TEST\_BASE\_CLIENT: Write basic unit tests (mocking API calls).

**Ticket ID:** NXS-1E-002

* **Title:** Implement query\_sonar\_online Method  
* **Checklist:**  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-002-DEFINE\_METHOD\_SIGNATURE: Define query\_sonar\_online(self, question: str) method in the client class.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-002-CONSTRUCT\_REQUEST\_PAYLOAD: Construct the JSON payload for the /chat/completions endpoint, specifying a sonar-online model (e.g., sonar-small-online, sonar-medium-online, or simply sonar if it defaults to online).14  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-002-CALL\_BASE\_REQUEST\_FUNCTION: Use the base request function from NXS-1E-001.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-002-EXTRACT\_ANSWER\_SOURCES: Extract the answer text and any source URLs/citations from the API response.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-002-DEFINE\_OUTPUT\_FORMAT: Define output (answer string, list of source URLs).  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-002-UNIT\_TEST\_SONAR\_ONLINE: Write unit tests (mocking API calls).

**Ticket ID:** NXS-1E-003

* **Title:** Implement query\_sonar\_research Method  
* **Checklist:**  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-003-DEFINE\_METHOD\_SIGNATURE: Define query\_sonar\_research(self, question: str) method.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-003-CONSTRUCT\_REQUEST\_PAYLOAD: Construct JSON payload, specifying a sonar-research model (e.g., sonar-deep-research).12  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-003-CALL\_BASE\_REQUEST\_FUNCTION: Use the base request function.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-003-EXTRACT\_ANSWER\_SOURCES: Extract answer and sources.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-003-DEFINE\_OUTPUT\_FORMAT: Define output.  
  * \[ \] WEBSEARCH\_DEV-NXS-1E-003-UNIT\_TEST\_SONAR\_RESEARCH: Write unit tests (mocking API calls).

---

**Phase 2: Build the Evaluation Framework (Agent: EVAL\_FRAMEWORK\_DEV)**

**Ticket ID:** NXS-2F-001

* **Title:** Design and Implement Multi-Module Test Harness Script  
* **Checklist:**  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-DEFINE\_MODULE\_INTERFACE: Define a common Python interface (e.g., an abstract base class) that all Phase 1 answering modules must implement (e.g., answer(question, xml\_path=None) returning (answer\_text, citations\_list)).  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-CREATE\_HARNESS\_SCRIPT\_STRUCTURE: Create the main evaluation script structure.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-IMPLEMENT\_MODULE\_INSTANTIATION: Implement logic to instantiate each Phase 1 module.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-IMPLEMENT\_MODULE\_INVOCATION\_LOOP: Loop through modules, call their answer method with the test question and XML path.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-IMPLEMENT\_DATA\_COLLECTION: Collect (module\_name, answer\_object, raw\_response) tuples.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-IMPLEMENT\_ERROR\_HANDLING: Add try-except blocks for individual module failures, log errors, and continue.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-COMMAND\_LINE\_ARGS: Add command-line arguments for test question and XML file path.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-001-UNIT\_TEST\_HARNESS: Test harness with mock modules.

**Ticket ID:** NXS-2F-002

* **Title:** Implement LLM-as-Judge Scoring Mechanism  
* **Checklist:**  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-DEFINE\_EVAL\_CRITERIA: Finalize evaluation criteria (Factual Accuracy, Relevance, Completeness, Citation Quality) and 1-10 scale.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-CHOOSE\_JUDGE\_LLM: Select judge LLM (e.g., Gemini 1.5 Pro, GPT-4).  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-CRAFT\_JUDGE\_PROMPT: Develop detailed prompt for the judge LLM, including criteria, scale, input format (question, answer, context), and desired JSON output format for scores/justifications.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-IMPLEMENT\_JUDGE\_LLM\_API\_CALL: Implement function to call the judge LLM API with the prompt and inputs.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-PARSE\_JUDGE\_RESPONSE: Implement logic to parse the judge LLM's JSON response to extract scores and justifications.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-INTEGRATE\_WITH\_HARNESS: Integrate this scoring function into the test harness script (NXS-2F-001) to score each collected answer.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-002-UNIT\_TEST\_SCORING: Test scoring mechanism with sample inputs/outputs (mock LLM judge).

**Ticket ID:** NXS-2F-003

* **Title:** Implement Comparative Performance Report Generation  
* **Checklist:**  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-003-DEFINE\_REPORT\_STRUCTURE: Define the structure of the markdown report.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-003-IMPLEMENT\_MARKDOWN\_GENERATION\_LOGIC: Write Python functions to generate markdown for:  
    * Original question.  
    * Each module's section (answer, scores, justifications).  
    * Aggregated summary table.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-003-INTEGRATE\_REPORTING\_INTO\_HARNESS: Call report generation function at the end of the test harness script (NXS-2F-001).  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-003-SAVE\_REPORT\_TO\_FILE: Implement saving the generated markdown to a file.  
  * \[ \] EVAL\_FRAMEWORK\_DEV-NXS-2F-003-UNIT\_TEST\_REPORTING: Test report generation with sample scored data.

---

**Phase 3: Design the Central Orchestrator (Agent: ORCHESTRATOR\_DEV)**

**Ticket ID:** NXS-3F-001

* **Title:** Design and Implement Orchestrator Class Core Structure  
* **Checklist:**  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-001-DEFINE\_ORCHESTRATOR\_CLASS: Define Orchestrator class.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-001-IMPLEMENT\_INITIALIZATION: \_\_init\_\_ to load/configure instances of all Phase 1 answering modules (using the common interface from NXS-2F-001-DEFINE\_MODULE\_INTERFACE).  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-001-IMPLEMENT\_MAIN\_QUERY\_METHOD: Implement a main method like process\_query(raw\_user\_question, source\_xml\_path=None) that will eventually house the full orchestration logic.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-001-CONFIG\_EXECUTION\_MODE: Add configuration for execution mode (concurrent/sequential).  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-001-UNIT\_TEST\_CORE\_STRUCTURE: Basic unit tests for instantiation and query intake.

**Ticket ID:** NXS-3F-002

* **Title:** Implement Concurrent Mode for Module Execution in Orchestrator  
* **Checklist:**  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-002-ADAPT\_MODULES\_FOR\_ASYNC: Ensure Phase 1 module answer methods can be called asynchronously (if they involve I/O, make them async def or wrap synchronous calls with asyncio.to\_thread).  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-002-IMPLEMENT\_ASYNCIO\_GATHER: In Orchestrator, use asyncio.gather to run selected module answer methods concurrently.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-002-HANDLE\_ASYNC\_RESULTS: Collect results (and potential exceptions) from asyncio.gather.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-002-INTEGRATE\_CONCURRENT\_MODE\_SWITCH: Integrate this logic into the main query method based on the execution mode config.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-002-UNIT\_TEST\_CONCURRENT\_MODE: Test concurrent execution with mock async modules.

**Ticket ID:** NXS-3F-003

* **Title:** Implement Sequential (Waterfall) Mode for Module Execution in Orchestrator  
* **Checklist:**  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-003-DEFINE\_DEFAULT\_SEQUENCE: Define the default waterfall sequence of modules.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-003-IMPLEMENT\_SEQUENTIAL\_LOOP: Implement a loop to execute modules one by one according to the sequence.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-003-OPTIONAL\_EARLY\_EXIT\_LOGIC: (Optional) Design and implement logic for early exit (e.g., based on a quick heuristic score of an intermediate answer).  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-003-INTEGRATE\_SEQUENTIAL\_MODE\_SWITCH: Integrate this logic into the main query method.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-003-UNIT\_TEST\_SEQUENTIAL\_MODE: Test sequential execution, including early exit if implemented.

**Ticket ID:** NXS-3F-004

* **Title:** Implement Real-time Answer Scoring Logic in Orchestrator  
* **Checklist:**  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-004-ADAPT\_PHASE2\_SCORING: Adapt the LLM-as-Judge logic from NXS-2F-002 for real-time use. Consider a faster/smaller judge LLM or simplified criteria.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-004-IMPLEMENT\_SCORING\_FUNCTION: Create a function within Orchestrator to score a list of answers.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-004-INTEGRATE\_SCORING\_POST\_EXECUTION: Call this scoring function after module(s) execution in both concurrent and sequential modes.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-004-UNIT\_TEST\_REALTIME\_SCORING: Test real-time scoring with sample answers.

**Ticket ID:** NXS-3F-005

* **Title:** Implement Answer Selection Strategy in Orchestrator  
* **Checklist:**  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-005-DESIGN\_SELECTION\_STRATEGY: Design the selection strategy (e.g., highest average score, weighted score).  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-005-IMPLEMENT\_SELECTION\_LOGIC: Implement the chosen selection logic to pick the best answer from the scored list.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-005-INTEGRATE\_SELECTION\_INTO\_FLOW: Integrate this after real-time scoring (NXS-3F-004).  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-005-UNIT\_TEST\_SELECTION: Test selection logic with various scored answer sets.

**Ticket ID:** NXS-3F-006

* **Title:** Implement Hybrid Answer Synthesis Logic in Orchestrator  
* **Checklist:**  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-CHOOSE\_SYNTHESIS\_LLM: Select an LLM for answer synthesis.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-CRAFT\_SYNTHESIS\_PROMPT: Develop a prompt for the synthesis LLM to combine insights from top 2-3 answers, ensuring coherence and accuracy.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-IMPLEMENT\_SYNTHESIS\_FUNCTION: Implement a function to call the synthesis LLM with the top answers and prompt.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-HANDLE\_SYNTHESIS\_CITATIONS: Address how citations from multiple sources will be handled/merged in the synthesized answer.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-ADD\_HYBRID\_MODE\_CONFIG: Add configuration to enable/disable hybrid answer mode.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-INTEGRATE\_SYNTHESIS\_INTO\_FLOW: If hybrid mode is enabled, call synthesis instead of simple selection.  
  * \[ \] ORCHESTRATOR\_DEV-NXS-3F-006-UNIT\_TEST\_SYNTHESIS: Test hybrid answer synthesis.

---

**Phase 4: Implement Agentic Prompt Optimization (Agent: PROMPT\_OPTIMIZER\_DEV)**

**Ticket ID:** NXS-4G-001

* **Title:** Design and Implement PromptOptimizer Class  
* **Checklist:**  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-001-DEFINE\_OPTIMIZER\_CLASS: Define PromptOptimizer class.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-001-IMPLEMENT\_INITIALIZATION: \_\_init\_\_ (e.g., to configure LLM for optimization).  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-001-DEFINE\_OPTIMIZE\_METHOD: Define main method optimize\_query(raw\_question: str, target\_module\_type: str \= None).  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-001-UNIT\_TEST\_CLASS\_STRUCTURE: Basic unit tests for instantiation.

**Ticket ID:** NXS-4G-002

* **Title:** Implement Magnetic RAG Algorithm in PromptOptimizer  
* **Checklist:**  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-002-CHOOSE\_OPTIMIZATION\_LLM: Select LLM for query rewriting.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-002-DEVELOP\_MAGNETIC\_RAG\_PROMPT: Develop few-shot prompts to instruct the LLM to rewrite the raw question into a detailed, explicit prompt with placeholder slots for evidence, as per the "Magnetic RAG" concept.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-002-IMPLEMENT\_LLM\_CALL\_FOR\_REWRITING: Implement the call to the optimization LLM within the optimize\_query method.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-002-PARSE\_OPTIMIZED\_PROMPT: Parse the LLM's output to get the structured optimized prompt.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-002-UNIT\_TEST\_MAGNETIC\_RAG: Test the Magnetic RAG rewriting with various raw questions.

**Ticket ID:** NXS-4G-003

* **Title:** Integrate PromptOptimizer into the Central Orchestrator  
* **Checklist:**  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-003-MODIFY\_ORCHESTRATOR\_INIT: Orchestrator (NXS-3F-001) to instantiate PromptOptimizer.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-003-MODIFY\_ORCHESTRATOR\_QUERY\_FLOW: In Orchestrator's process\_query method, call prompt\_optimizer.optimize\_query() with the raw user question before passing it to expert modules.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-003-HANDLE\_TAILORED\_PROMPTS: (If applicable) Implement logic in PromptOptimizer or Orchestrator to tailor the optimized prompt based on target\_module\_type.  
  * \[ \] PROMPT\_OPTIMIZER\_DEV-NXS-4G-003-END\_TO\_END\_TEST\_WITH\_OPTIMIZER: Test the full Orchestrator flow with prompt optimization integrated.

---

**Phase 5: Construct the Streamlit Web Interface (Agent: UI\_UX\_DEPLOY\_DEV)**

**Ticket ID:** NXS-5H-001

* **Title:** Develop Main Streamlit App File and Basic Chat Interface  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-001-CREATE\_STREAMLIT\_APP\_FILE: Create app.py (or similar).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-001-INITIALIZE\_CHAT\_HISTORY: Initialize st.session\_state.messages if not exists.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-001-DISPLAY\_PRIOR\_MESSAGES: Loop through st.session\_state.messages and display using st.chat\_message.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-001-IMPLEMENT\_USER\_INPUT: Use st.chat\_input() to get user query.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-001-ADD\_USER\_MESSAGE\_TO\_HISTORY: Append user message to st.session\_state.messages and display it.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-001-PLACEHOLDER\_ASSISTANT\_RESPONSE: Add placeholder for assistant response.

**Ticket ID:** NXS-5H-002

* **Title:** Implement Backend Orchestrator Invocation from Streamlit  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-002-IMPORT\_ORCHESTRATOR: Import the Orchestrator class.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-002-INSTANTIATE\_ORCHESTRATOR: Instantiate the Orchestrator (likely once, stored in st.session\_state or globally).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-002-DEFINE\_BACKEND\_CALL\_FUNCTION: Create a function that takes user query and calls orchestrator.process\_query().  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-002-RUN\_ORCHESTRATOR\_IN\_THREAD: Use threading.Thread to run the backend call function to avoid blocking UI.20  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-002-RETRIEVE\_FINAL\_ANSWER: Implement mechanism to get the final answer back from the thread (e.g., via a shared queue or by joining the thread and checking a return value).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-002-DISPLAY\_ASSISTANT\_RESPONSE: Display the Orchestrator's response using st.chat\_message and add to history.

**Ticket ID:** NXS-5H-003

* **Title:** Implement Real-time Progress Status Indicator in Streamlit  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-003-MODIFY\_ORCHESTRATOR\_FOR\_UPDATES: Orchestrator to push status strings to a thread-safe queue.Queue.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-003-CREATE\_STATUS\_PLACEHOLDER: In Streamlit, use status\_container \= st.status("Processing query...", expanded=True) or progress\_placeholder \= st.empty().21  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-003-IMPLEMENT\_POLLING\_LOOP: After starting the backend thread, implement a while loop in Streamlit to:  
    * Try to get a message from the progress queue (non-blocking).  
    * If message received, update status\_container.write(message) or progress\_placeholder.text(message).  
    * If a completion signal (e.g., None) is received from queue, break loop and update status to complete.  
    * time.sleep(0.1) to prevent busy-waiting.20  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-003-TEST\_PROGRESS\_UPDATES: Test with an Orchestrator that sends multiple progress messages.

**Ticket ID:** NXS-5H-004

* **Title:** Implement Response Streaming using st.write\_stream in Streamlit  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-004-MODIFY\_ORCHESTRATOR\_FOR\_STREAMING: Orchestrator's final answer generation (especially synthesis LLM call) to be a Python generator function (yielding tokens/chunks).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-004-GET\_STREAM\_GENERATOR: In Streamlit, after Orchestrator processing is complete (or as part of it), get this generator function.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-004-USE\_ST\_WRITE\_STREAM: Within an assistant st.chat\_message block, call st.write\_stream(response\_generator).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-004-CAPTURE\_FULL\_STREAMED\_RESPONSE: Collect the full streamed response to save to chat history.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-5H-004-TEST\_STREAMING: Test with an Orchestrator that streams its final output.

---

**Phase 6: Finalize as a Production-Ready, Multi-User Website (Agent: UI\_UX\_DEPLOY\_DEV)**

**Ticket ID:** NXS-6H-001

* **Title:** Design Database Schema for User Accounts and Chat History  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-001-DEFINE\_USERS\_TABLE: Define Users table schema (user\_id PK, username, email, hashed\_password, salt, role, created\_at).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-001-DEFINE\_CHATSESSIONS\_TABLE: Define ChatSessions table schema (session\_id PK, user\_id FK, session\_name, created\_at, last\_updated\_at).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-001-DEFINE\_CHATMESSAGES\_TABLE: Define ChatMessages table schema (message\_id PK, session\_id FK, timestamp, role, content).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-001-CHOOSE\_DB\_TYPES: Select appropriate SQL data types for SQLite and PostgreSQL.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-001-DOCUMENT\_SCHEMA: Document the schema.

**Ticket ID:** NXS-6H-002

* **Title:** Implement Database Integration Layer (ORM)  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-002-SETUP\_SQLALCHEMY: Install SQLAlchemy.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-002-DEFINE\_ORM\_MODELS: Create SQLAlchemy ORM models for Users, ChatSessions, ChatMessages based on NXS-6H-001.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-002-SETUP\_DB\_CONNECTION: Implement logic for database connection (SQLite for dev, PostgreSQL for prod).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-002-CREATE\_DB\_SESSION\_MANAGEMENT: Implement SQLAlchemy session management.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-002-IMPLEMENT\_CRUD\_UTILS: Implement basic CRUD utility functions for each model (e.g., get\_user\_by\_email, create\_chat\_session).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-002-INITIALIZE\_DATABASE\_SCRIPT: Create a script to initialize the database schema.

**Ticket ID:** NXS-6H-003

* **Title:** Implement User Account Management Backend Logic  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-003-IMPLEMENT\_PASSWORD\_HASHING: Implement password hashing (e.g., werkzeug.security).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-003-IMPLEMENT\_USER\_CREATION: Implement function create\_user(email, password, username, role='user') using ORM (NXS-6H-002).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-003-IMPLEMENT\_USER\_RETRIEVAL: Implement get\_user\_by\_email(email) and get\_user\_by\_id(user\_id).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-003-IMPLEMENT\_PASSWORD\_VERIFICATION: Implement check\_password(user, password).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-003-IMPLEMENT\_ROLE\_UPDATE: Implement function to update user role.

**Ticket ID:** NXS-6H-004

* **Title:** Implement Chat History Storage and Retrieval Backend Logic  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-004-IMPLEMENT\_CREATE\_SESSION: Implement create\_chat\_session(user\_id, session\_name=None) using ORM.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-004-IMPLEMENT\_ADD\_MESSAGE: Implement add\_chat\_message(session\_id, role, content) using ORM.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-004-IMPLEMENT\_GET\_SESSION\_MESSAGES: Implement get\_messages\_for\_session(session\_id).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-004-IMPLEMENT\_GET\_USER\_SESSIONS: Implement get\_sessions\_for\_user(user\_id).

**Ticket ID:** NXS-6H-005

* **Title:** Implement Streamlit User Authentication (OIDC)  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-SETUP\_OIDC\_PROVIDER: Set up a chosen OIDC provider (e.g., Google, Auth0).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-CONFIGURE\_SECRETS\_TOML: Configure secrets.toml with OIDC client\_id, client\_secret, server\_metadata\_url, redirect\_uri, cookie\_secret.22  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-IMPLEMENT\_LOGIN\_BUTTON: Add st.button("Login", on\_click=st.login) or provider-specific login buttons.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-CHECK\_LOGIN\_STATUS: Use if not st.user.is\_logged\_in: to control access.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-DISPLAY\_USER\_INFO: Display st.user.name or st.user.email for logged-in users.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-IMPLEMENT\_LOGOUT\_BUTTON: Add st.button("Logout", on\_click=st.logout).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-005-LINK\_OIDC\_TO\_DB\_USER: After OIDC login, check if st.user.email exists in local DB (NXS-6H-003); if not, create a new user entry. Store local user\_id in st.session\_state.

**Ticket ID:** NXS-6H-006

* **Title:** Create Admin-Only Pages in Streamlit  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-006-CREATE\_PAGES\_DIR: Create pages/ directory for multipage app.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-006-CREATE\_ADMIN\_PAGE\_FILE: Create pages/admin\_dashboard.py (or similar).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-006-IMPLEMENT\_ROLE\_CHECK: In admin\_dashboard.py, retrieve user's role (from st.session\_state.user\_role or by querying DB with st.session\_state.user\_id from NXS-6H-005) and deny access if not 'admin'.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-006-DESIGN\_ADMIN\_LAYOUT: Basic layout for admin functions (e.g., tabs for user management, document upload).

**Ticket ID:** NXS-6H-007

* **Title:** Implement Admin Upload Feature UI (XML & PDF)  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-007-ADD\_FILE\_UPLOADER: In an admin page (NXS-6H-006), use st.file\_uploader(accept\_multiple\_files=True, type=\['xml', 'pdf'\]).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-007-HANDLE\_UPLOADED\_FILES: When files are uploaded, get their content/bytes.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-007-TRIGGER\_BACKEND\_PROCESSING: Pass uploaded file data to the asynchronous backend task (NXS-6I-002).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-007-DISPLAY\_UPLOAD\_STATUS: Show status messages for uploads (e.g., "File enqueued for processing").

**Ticket ID:** NXS-6H-008

* **Title:** Implement Chat History Display UI for Users  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-008-FETCH\_USER\_SESSIONS: On login/app load for authenticated user, call backend (NXS-6H-004) to get their past chat sessions.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-008-DISPLAY\_SESSION\_LIST: Display list of sessions in a sidebar or dropdown (e.g., using st.selectbox or st.radio).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-008-LOAD\_SELECTED\_SESSION: When a session is selected:  
    * Call backend (NXS-6H-004) to get messages for that session.  
    * Populate st.session\_state.messages with these messages.  
    * Rerun app to display the loaded chat.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6H-008-HANDLE\_NEW\_CHAT\_SESSION: Logic to start a new chat session if no history is selected or user initiates a new one.

**Ticket ID:** NXS-6I-001

* **Title:** Implement PDF Parsing Module  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-001-INSTALL\_PYMUPDF: Install PyMuPDF (pip install PyMuPDF).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-001-DEFINE\_PDF\_PARSE\_FUNCTION: Create extract\_text\_from\_pdf(pdf\_file\_path\_or\_bytes) function.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-001-IMPLEMENT\_PYMUPDF\_LOGIC: Use fitz.open() and loop through pages to page.get\_text().23  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-001-HANDLE\_PARSING\_ERRORS: Add error handling for corrupted PDFs.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-001-RETURN\_EXTRACTED\_TEXT: Return the concatenated text.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-001-UNIT\_TEST\_PDF\_PARSING: Test with a sample PDF file.

**Ticket ID:** NXS-6I-002

* **Title:** Implement Asynchronous Backend Task for Knowledge Store Updates  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-CHOOSE\_ASYNC\_FRAMEWORK: Choose async task framework (Celery, concurrent.futures, or FastAPI background tasks).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-DEFINE\_INGESTION\_TASK\_FUNCTION: Define the main ingestion task function that takes document data (path or bytes, type).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-INTEGRATE\_PARSERS: Inside the task, call NXS-1Z-001 (XML) or NXS-6I-001 (PDF) parser.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-DEFINE\_MODULE\_UPDATE\_INTERFACES: Ensure each Phase 1 document-based module has an update\_knowledge\_store(parsed\_document\_content) method.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-CALL\_MODULE\_UPDATES: In the task, loop through relevant modules and call their update methods.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-IMPLEMENT\_STATUS\_TRACKING: Implement a way to track task status (e.g., in DB or a shared cache) for admin UI feedback.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-CONNECT\_UPLOAD\_TO\_TASK\_QUEUE: Admin upload (NXS-6H-007) should enqueue this task.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6I-002-TEST\_ASYNC\_INGESTION: Test the full async ingestion pipeline.

**Ticket ID:** NXS-6J-001

* **Title:** Prepare Streamlit Application for Production Deployment  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-001-CREATE\_CONFIG\_TOML: Create/update .streamlit/config.toml.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-001-SET\_SERVER\_HEADLESS: Set \[server\]\\nheadless \= true.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-001-CONFIGURE\_LOGGING: Set \[logger\]\\nlevel \= "info" (or warning).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-001-SET\_MAX\_UPLOAD\_SIZE: Configure \[server\]\\nmaxUploadSize if needed.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-001-FINALIZE\_REQUIREMENTS\_TXT: Ensure requirements.txt has all dependencies with pinned versions.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-001-REVIEW\_SECRETS\_HANDLING: Ensure API keys and secrets are loaded from environment variables or secrets.toml and not hardcoded.

**Ticket ID:** NXS-6J-002

* **Title:** Create Sample NGINX Configuration for Reverse Proxy  
* **Checklist:**  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-CREATE\_NGINX\_CONF\_FILE: Create a sample nginx.conf file.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-CONFIGURE\_LISTEN\_PORTS: Configure listen 80; and listen 443 ssl;.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-CONFIGURE\_SERVER\_NAME: Set server\_name your\_domain.com;.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-ADD\_SSL\_CONFIG: Add placeholders/examples for ssl\_certificate and ssl\_certificate\_key.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-CONFIGURE\_PROXY\_PASS: Configure location / { proxy\_pass http://localhost:8501/; } (assuming Streamlit runs on 8501).  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-SET\_PROXY\_HEADERS: Set necessary headers: proxy\_set\_header Host $host;, proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-CONFIGURE\_WEBSOCKET\_PROXYING: Crucially, add WebSocket headers for /stream and /stcore/stream or general location: proxy\_http\_version 1.1; proxy\_set\_header Upgrade $http\_upgrade; proxy\_set\_header Connection "upgrade";.25  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-SET\_TIMEOUTS: Set proxy\_read\_timeout to a reasonable value.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-ADD\_COMMENTS\_INSTRUCTIONS: Add comments explaining the configuration.  
  * \[ \] UI\_UX\_DEPLOY\_DEV-NXS-6J-002-TEST\_NGINX\_CONFIG\_LOCALLY: (Optional, if possible) Test the NGINX config with a local Streamlit app.