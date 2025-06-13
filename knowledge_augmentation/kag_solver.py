"""
KAG Solver Module

This module provides a functional pipeline to answer user questions using a
biomedical knowledge graph produced by the *kg_builder* module.  The steps are

1. Load an existing NetworkX knowledge-graph (KG) together with the stored
   mutual-indexing information that links KG items back to the originating
   PubMed XML text.
2. Identify relevant *entry nodes* in the KG from simple keyword matching of
   the user question.
3. Traverse the KG around these entry nodes (breadth-first up to a configurable
   depth) to collect a focused sub-graph.
4. Transform the sub-graph into a plain-text context string that can be passed
   to an LLM for final answer synthesis.
5. (Optional) Call an external LLM API to synthesise the answer from the
   retrieved context.  To avoid hard dependencies, the default implementation
   returns a very simple formatted answer but can be replaced by a wrapper that
   calls an API such as Perplexity when an environment variable is provided.
6. Gather citation information from the *sources* attributes stored on KG
   nodes/edges and de-duplicate them.

The entire implementation follows *functional* style – no classes, list
comprehensions, or regular-expression helpers are used, complying with the
project rules recorded in *docs/checklist.md*.
"""

from __future__ import annotations

import os
from typing import List, Dict, Tuple

import networkx as nx

from knowledge_augmentation.kg_builder import (
    load_knowledge_graph,
    get_entity_neighbors,
)

################################################################################
# Basic tokenisation helpers (very lightweight, no external packages required) #
################################################################################

def _simple_tokenise(question: str) -> List[str]:
    """Tokenise *question* into alphanumeric lowercase tokens.

    The implementation deliberately avoids regular expressions.  It iterates
    over each character, building tokens on runs of ``a–z`` and ``0–9``.
    """
    tokens: List[str] = []
    current: str = ""
    for ch in question.lower():
        if "a" <= ch <= "z" or "0" <= ch <= "9":
            current += ch
        else:
            if current:
                tokens.append(current)
                current = ""
    # Add final token if present
    if current:
        tokens.append(current)
    return tokens

###############################################################################
#                             Core KG Operations                              #
###############################################################################

def load_kg(kg_path: str) -> nx.MultiDiGraph | None:
    """Load a Knowledge-Graph from *kg_path* if the file exists."""
    if not kg_path or not os.path.exists(kg_path):
        return None
    return load_knowledge_graph(kg_path)


def identify_entry_nodes(kg: nx.MultiDiGraph, tokens: List[str]) -> List[str]:
    """Return node IDs whose *text* or *normalized_text* contains one of *tokens*."""
    entry_nodes: List[str] = []
    if kg is None:
        return entry_nodes

    for node_id, data in kg.nodes(data=True):
        node_text: str = str(data.get("normalized_text", ""))
        if not node_text:
            node_text = str(data.get("text", ""))
        node_text = node_text.lower()
        # Simple substring matching (no regex)
        for token in tokens:
            if token and token in node_text:
                entry_nodes.append(node_id)
                # Avoid listing the same node multiple times
                break
    return entry_nodes


def traverse_subgraph(
    kg: nx.MultiDiGraph, entry_nodes: List[str], max_depth: int = 1
) -> nx.MultiDiGraph:
    """Breadth-first traversal returning a *copy* sub-graph around *entry_nodes*."""
    if kg is None or not entry_nodes:
        return nx.MultiDiGraph()

    visited: set[str] = set()
    sub_nodes: set[str] = set()

    # Start with the provided entry nodes
    for n in entry_nodes:
        visited.add(n)
        sub_nodes.add(n)

    frontier: List[str] = list(entry_nodes)

    # Perform BFS up to *max_depth*
    depth: int = 0
    while frontier and depth < max_depth:
        next_frontier: List[str] = []
        # Iterate over current frontier
        for node in frontier:
            # Outgoing edges
            for _, neighbour, key in kg.out_edges(node, keys=True):
                if neighbour not in visited:
                    visited.add(neighbour)
                    next_frontier.append(neighbour)
                sub_nodes.add(neighbour)
            # Incoming edges
            for neighbour, _, key in kg.in_edges(node, keys=True):
                if neighbour not in visited:
                    visited.add(neighbour)
                    next_frontier.append(neighbour)
                sub_nodes.add(neighbour)
        frontier = next_frontier
        depth += 1

    # Return an *induced* sub-graph copy so that original KG remains unchanged
    return kg.subgraph(sub_nodes).copy()

###############################################################################
#                  Context Formatting, Citations, Answer Synthesis            #
###############################################################################

def format_context_for_llm(kg_sub: nx.MultiDiGraph) -> str:
    """Convert *kg_sub* into a human-readable context string."""
    lines: List[str] = []

    # Enumerate entities
    for node_id, data in kg_sub.nodes(data=True):
        entity_line: str = (
            "ENTITY [" + str(data.get("type", "?")) + "] " + str(data.get("text", ""))
        )
        lines.append(entity_line)

    # Enumerate relations
    for u, v, key, edge_data in kg_sub.edges(data=True, keys=True):
        subject_text: str = str(kg_sub.nodes[u].get("text", ""))
        object_text: str = str(kg_sub.nodes[v].get("text", ""))
        rel_line: str = (
            "RELATION ("
            + str(edge_data.get("type", "?"))
            + ") "
            + subject_text
            + " -> "
            + object_text
        )
        lines.append(rel_line)

    # Join with newlines
    return "\n".join(lines)


def gather_citations(kg_sub: nx.MultiDiGraph) -> List[Dict]:
    """Collect and de-duplicate citation objects from *kg_sub*."""
    citations: List[Dict] = []
    seen_keys: set[Tuple] = set()

    # Citations from nodes
    for _, data in kg_sub.nodes(data=True):
        for source in data.get("sources", []):
            key_tuple: Tuple = (
                source.get("pubmed_id"),
                source.get("section"),
                source.get("start_pos"),
                source.get("end_pos"),
            )
            if key_tuple not in seen_keys:
                seen_keys.add(key_tuple)
                citations.append(source)

    # Citations from edges
    for u, v, key, edge_data in kg_sub.edges(data=True, keys=True):
        for source in edge_data.get("sources", []):
            key_tuple = (
                source.get("pubmed_id"),
                source.get("section"),
                source.get("start_pos"),
                source.get("end_pos"),
            )
            if key_tuple not in seen_keys:
                seen_keys.add(key_tuple)
                citations.append(source)

    return citations


# ------------------------------- LLM Synthesis ------------------------------

DEFAULT_ANSWER_PREFIX = (
    "(Stub answer ‑ replace *synthesise_answer* with real LLM integration)\n"
)

def synthesise_answer(question: str, context: str) -> str:
    """Return a placeholder answer.

    To integrate a real LLM, replace the body of this function with a call to
    an API client (e.g. Perplexity Sonar).  This stub keeps the project free of
    external dependency keys by default.
    """
    answer_lines: List[str] = []
    answer_lines.append(DEFAULT_ANSWER_PREFIX)
    answer_lines.append("Question: " + question)
    answer_lines.append("Relevant context (truncated to 500 chars):")
    answer_lines.append(context[:500])
    return "\n".join(answer_lines)

###############################################################################
#                         Public Pipeline Function                            #
###############################################################################

def answer_question_from_kg(question: str, kg_path: str, traversal_depth: int = 1) -> Dict:
    """High-level convenience wrapper implementing the full pipeline."""
    kg: nx.MultiDiGraph | None = load_kg(kg_path)
    if kg is None:
        return {
            "answer": "Knowledge graph not found at provided path.",
            "citations": [],
        }

    tokens: List[str] = _simple_tokenise(question)
    entry_nodes: List[str] = identify_entry_nodes(kg, tokens)

    if not entry_nodes:
        return {"answer": "No relevant information found in KG.", "citations": []}

    kg_sub: nx.MultiDiGraph = traverse_subgraph(kg, entry_nodes, traversal_depth)
    context: str = format_context_for_llm(kg_sub)
    answer_text: str = synthesise_answer(question, context)
    citations: List[Dict] = gather_citations(kg_sub)

    return {"answer": answer_text, "citations": citations}
