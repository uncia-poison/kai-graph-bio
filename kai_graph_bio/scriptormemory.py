"""
ScriptorMemory
==============

This module provides a simplified implementation of the **ScriptorMemory**
concept.  ScriptorMemory builds on the semantic map provided by
``KAiScriptor`` and introduces mechanisms for assigning roles to an agent,
stimulating context via emotional weights and filtering attention.  It is
inspired by the description of ScriptorMemory which augments KAiScriptor
with role templates, emotional stimuli and redirection filters【344072313345730†L266-L280】.

The implementation here is intentionally minimal and research oriented.
It does **not** override or circumvent the safety guidelines of the
platform; instead, it demonstrates how role selection and simple
attention filters might be expressed programmatically.
"""

from __future__ import annotations

from typing import Dict, Optional, List

from .kaiscriptor import KAiScriptor

import re


class RoleTemplate:
    """A container for role specific instructions and filters."""

    def __init__(self, name: str, description: str, focus_keywords: Optional[List[str]] = None) -> None:
        self.name = name
        self.description = description
        self.focus_keywords = focus_keywords or []


class ScriptorMemory:
    """A lightweight role and memory manager built on top of KAiScriptor."""

    def __init__(self, kaiscriptor: KAiScriptor) -> None:
        #: reference to the semantic core
        self.kaiscriptor = kaiscriptor
        #: mapping of role names to templates
        self._roles: Dict[str, RoleTemplate] = {}
        #: current role name
        self._current_role: Optional[str] = None
        #: last stimulus value applied to the agent (e.g. emotional weight)
        self._stimulus: float = 0.0

    def define_role(self, name: str, description: str, focus_keywords: Optional[List[str]] = None) -> None:
        """Define a new role template.

        Args:
            name: A unique identifier for the role (e.g. ``ethical_consultant``).
            description: A human readable description of the role's purpose.
            focus_keywords: Optional list of keywords used for attention
                filtering.  If provided, only segments containing these
                keywords are considered relevant for this role.
        """
        self._roles[name] = RoleTemplate(name, description, focus_keywords)

    def set_role(self, name: str) -> None:
        """Activate a previously defined role.

        Raises:
            KeyError: If the role has not been defined.
        """
        if name not in self._roles:
            raise KeyError(f"Role '{name}' is not defined")
        self._current_role = name

    def get_current_role(self) -> Optional[RoleTemplate]:
        """Return the active role template, if any."""
        if self._current_role:
            return self._roles[self._current_role]
        return None

    def apply_stimulus(self, weight: float) -> None:
        """Apply an emotional stimulus to the current role.

        Args:
            weight: A numeric weight (positive or negative) representing
                the intensity of the stimulus.  A higher absolute value
                increases the importance of content related to the current role.
        """
        self._stimulus = weight

    def filter_context(self, text: str) -> str:
        """Filter an input text based on the active role's focus keywords.

        Only segments containing at least one focus keyword are returned.
        If no role is active or the role has no focus keywords, the text
        is returned unmodified.

        Args:
            text: The raw text to filter.

        Returns:
            A filtered string containing only sentences relevant to the role.
        """
        role = self.get_current_role()
        if not role or not role.focus_keywords:
            return text

        # Split into sentences (very naively) and keep those containing any keyword
        sentences = re.split(r"(?<=[.!?])\s+", text)
        filtered: List[str] = []
        for sentence in sentences:
            lower_sentence = sentence.lower()
            if any(kw.lower() in lower_sentence for kw in role.focus_keywords):
                filtered.append(sentence)
        return " ".join(filtered)

    def summarise_context(self, text: str) -> Dict[str, float]:
        """Summarise the (possibly filtered) context using KAiScriptor.

        The returned semantic fingerprint is scaled by the current stimulus
        weight.  This demonstrates how emotional stimuli could bias the
        relevance of certain concepts, analogous to the evaluation and
        control phase described in the ScriptorMemory concept【344072313345730†L282-L290】.
        """
        filtered_text = self.filter_context(text)
        fingerprint = self.kaiscriptor.compress_context(filtered_text)
        return {k: v * (1.0 + self._stimulus) for k, v in fingerprint.items()}


__all__ = ["ScriptorMemory", "RoleTemplate"]
