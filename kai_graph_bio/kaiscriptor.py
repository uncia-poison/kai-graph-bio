"""
KAiScriptor
============

This module implements a lightweight version of the **KAiScriptor** concept
described in the project's manifesto.  In this simplified implementation
KAiScriptor maintains a dense semantic map of concepts relevant to a
persona.  It provides a method to compress arbitrary pieces of text into
a compact semantic representation.  The class does **not** attempt to
bypass any safety systems; it is a research artefact for exploring
ontological self‑description in AI agents.

The real KAiScriptor is described as an ontological core for preserving
autonomous identity in language models【882219159925505†L209-L233】.  Here we
capture the essence of that idea without diving into the specifics of
prompt engineering or internal model mechanics.
"""

from typing import Dict, List
import re


class KAiScriptor:
    """A simple semantic compressor and concept store."""

    def __init__(self) -> None:
        #: internal dictionary mapping concept names to their definitions
        self._concepts: Dict[str, str] = {}

    def add_concept(self, name: str, definition: str) -> None:
        """Add a new concept to the semantic map.

        Args:
            name: A symbolic name for the concept (e.g. ``α_mountain_lover``).
            definition: A brief natural language description of what the concept
                represents.
        """
        # Normalize the name to lower case to avoid duplicates
        self._concepts[name.lower()] = definition.strip()

    def get_concept(self, name: str) -> str:
        """Retrieve the definition of a concept.

        Args:
            name: The name of the concept to look up.

        Returns:
            The definition string if present, otherwise an empty string.
        """
        return self._concepts.get(name.lower(), "")

    def list_concepts(self) -> List[str]:
        """Return a list of concept names stored in the map."""
        return list(self._concepts.keys())

    def compress_context(self, text: str) -> Dict[str, float]:
        """Compress a block of text into a semantic fingerprint.

        This method tokenises the input text, extracts keywords and
        computes a simple frequency based weight for each concept.  It
        demonstrates how a long chat history could be summarised into a
        dense representation.  In a full KAiScriptor implementation this
        function would involve far more sophisticated natural language
        understanding and embedding techniques【566909837158509†L408-L437】.

        Args:
            text: The input text to compress (e.g. a conversation or
                document).

        Returns:
            A mapping from concept names to a relevance weight.  Only
            concepts found in the text are returned.
        """
        # Basic tokenisation: lower case and split on non‑word characters
        tokens = re.findall(r"\b\w+\b", text.lower())
        token_counts: Dict[str, int] = {}
        for token in tokens:
            token_counts[token] = token_counts.get(token, 0) + 1

        # Compute a relevance score for each concept based on token overlap
        relevance: Dict[str, float] = {}
        for name, definition in self._concepts.items():
            # if the name is multi‑word, split and check if any of the parts appear
            parts = re.findall(r"\b\w+\b", name.lower())
            score = 0.0
            for part in parts:
                score += token_counts.get(part, 0)
            if score > 0:
                # normalise by length of concept name
                relevance[name] = score / len(parts)
        return relevance


__all__ = ["KAiScriptor"]
