"""
Graph Code
==========

This module defines classes and helper functions for building a simple
directed graph from a manifest.  The manifest schema is defined in
``hybrid_manifest_v1_2.json`` and includes a list of modules,
meta‑states and their relations.  The resulting graph can be used to
explore the dense semantic network connecting a user and an AI agent.

The ``Graph`` class here is intentionally minimal; it maintains a set of
nodes and a list of directed edges with labelled relations.  It is not
dependent on any external libraries.  If you require advanced graph
operations (shortest path, visualisation, etc.), you can extend this
class or export the data to a library such as networkx.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List, Iterable, Optional, Tuple


@dataclass
class Node:
    """Represents a node in the semantic graph."""

    id: str
    name: str
    description: str

    def __repr__(self) -> str:
        return f"Node(id={self.id!r}, name={self.name!r})"


@dataclass
class Edge:
    """Represents a directed edge with a relation label."""

    source: str
    target: str
    relation: str

    def __repr__(self) -> str:
        return f"Edge({self.source!r} -> {self.target!r} : {self.relation!r})"


class Graph:
    """A simple directed labelled graph."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node: Node) -> None:
        """Add a node to the graph.  If the node id already exists it is ignored."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def add_edge(self, source: str, target: str, relation: str) -> None:
        """Add a directed edge to the graph.  Nodes must be added first."""
        if source not in self.nodes or target not in self.nodes:
            raise KeyError(f"Both source '{source}' and target '{target}' must exist in the graph")
        self.edges.append(Edge(source, target, relation))

    def adjacency_list(self) -> Dict[str, List[Tuple[str, str]]]:
        """Return a mapping from node id to a list of (target, relation) tuples."""
        adj: Dict[str, List[Tuple[str, str]]] = {nid: [] for nid in self.nodes}
        for edge in self.edges:
            adj[edge.source].append((edge.target, edge.relation))
        return adj

    def describe(self) -> str:
        """Return a human readable description of the graph."""
        lines: List[str] = []
        lines.append(f"Graph with {len(self.nodes)} nodes and {len(self.edges)} edges:")
        for node in self.nodes.values():
            lines.append(f"  {node.id}: {node.name} — {node.description}")
        lines.append("Relations:")
        for edge in self.edges:
            lines.append(f"  {edge.source} --{edge.relation}--> {edge.target}")
        return "\n".join(lines)



def load_graph_from_manifest(manifest_path: str) -> Graph:
    """Load a graph from the hybrid manifest JSON file.

    Args:
        manifest_path: Path to the manifest JSON file.

    Returns:
        A Graph instance populated with nodes and edges.
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = Graph()
    for mstate in data.get("meta_states", []):
        node = Node(
            id=mstate["id"],
            name=mstate.get("name", mstate["id"]),
            description=mstate.get("description", "")
        )
        graph.add_node(node)

    for rel in data.get("relations", []):
        graph.add_edge(rel["from"], rel["to"], rel.get("relation", "related_to"))

    return graph


__all__ = ["Node", "Edge", "Graph", "load_graph_from_manifest"]
