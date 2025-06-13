"""Unit tests for kag_solver pipeline."""

import os
import tempfile
import networkx as nx

from knowledge_augmentation.kg_builder import create_knowledge_graph, add_entity_to_graph
from knowledge_augmentation.kag_solver import (
    answer_question_from_kg,
    _simple_tokenise,
    identify_entry_nodes,
    traverse_subgraph,
)


def _build_dummy_kg() -> nx.MultiDiGraph:
    """Create a tiny KG with a few nodes and relations for testing."""
    kg = create_knowledge_graph()
    # Manually add a couple of entities
    n1 = add_entity_to_graph(
        kg,
        {
            "type": "DISEASE",
            "text": "Diabetes Mellitus",
            "normalized_text": "diabetes mellitus",
        },
    )
    n2 = add_entity_to_graph(
        kg,
        {
            "type": "GENE",
            "text": "INS",
            "normalized_text": "ins",
        },
    )
    # Add a simple edge
    kg.add_edge(n1, n2, type="related_to", sources=[])
    return kg


def test_simple_tokenise():
    assert _simple_tokenise("Insulin regulates glucose.") == [
        "insulin",
        "regulates",
        "glucose",
    ]


def test_identify_entry_nodes():
    kg = _build_dummy_kg()
    tokens = ["diabetes", "unknown"]
    entries = identify_entry_nodes(kg, tokens)
    assert entries, "Expected to find at least one entry node"


def test_traverse_subgraph_depth_0():
    kg = _build_dummy_kg()
    sub = traverse_subgraph(kg, list(kg.nodes), 0)
    assert sub.number_of_nodes() == len(kg.nodes)


def test_answer_question_from_kg():
    kg = _build_dummy_kg()
    with tempfile.TemporaryDirectory() as tmpdir:
        kg_path = os.path.join(tmpdir, "kg.json")
        # Save using kg_builder helper
        from knowledge_augmentation.kg_builder import save_knowledge_graph

        save_knowledge_graph(kg, kg_path)
        result = answer_question_from_kg("What genes are related to diabetes?", kg_path)
        assert "answer" in result and "citations" in result

