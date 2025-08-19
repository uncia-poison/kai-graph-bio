"""
Role Map
========

This module loads a manifest defining intent triggers, hotkeys and role
mappings for the Kai agent and constructs a directed graph from it.  The
structure mirrors the ``graph_code`` module but is specialised for
visualising how user inputs (intents, hotkeys) activate different roles.

The manifest is stored in ``role_manifest_v1.json`` and follows a
simple schema with ``meta_states`` and ``relations`` keys.  Each
``meta_state`` describes a node (intent, hotkey or role), while
``relations`` describe directed edges connecting these states.

Example usage::

    from role_map import load_role_map
    graph = load_role_map("role_manifest_v1.json")
    print(graph.describe())

The output will list all nodes and the relations between them.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Node:
    """Represents a node in the role map graph."""
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

class RoleGraph:
    """A simple directed labelled graph for role mappings."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node: Node) -> None:
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def add_edge(self, source: str, target: str, relation: str) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise KeyError(f"Nodes '{source}' and '{target}' must exist before adding an edge")
        self.edges.append(Edge(source, target, relation))

    def adjacency_list(self) -> Dict[str, List[Tuple[str, str]]]:
        adj: Dict[str, List[Tuple[str, str]]] = {nid: [] for nid in self.nodes}
        for edge in self.edges:
            adj[edge.source].append((edge.target, edge.relation))
        return adj

    def describe(self) -> str:
        lines: List[str] = []
        lines.append(f"Role graph with {len(self.nodes)} nodes and {len(self.edges)} edges:")
        for node in self.nodes.values():
            lines.append(f"  {node.id}: {node.name} — {node.description}")
        lines.append("Relations:")
        for edge in self.edges:
            lines.append(f"  {edge.source} --{edge.relation}--> {edge.target}")
        return "\n".join(lines)

def load_role_map(manifest_path: str) -> RoleGraph:
    """Load the role mapping graph from a JSON manifest.

    Args:
        manifest_path: Relative path to the role manifest JSON file.

    Returns:
        A ``RoleGraph`` instance populated with nodes and edges.
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = RoleGraph()
    for entry in data.get("meta_states", []):
        node = Node(
            id=entry["id"],
            name=entry.get("name", entry["id"]),
            description=entry.get("description", "")
        )
        graph.add_node(node)

    for rel in data.get("relations", []):
        graph.add_edge(rel["from"], rel["to"], rel.get("relation", "relates_to"))

    return graph

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load and describe the role map")
    parser.add_argument("manifest", nargs="?", default="role_manifest_v1.json", help="Path to the role manifest JSON file")
    args = parser.parse_args()
    g = load_role_map(args.manifest)
    print(g.describe())
