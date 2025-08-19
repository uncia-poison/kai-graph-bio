"""
KaiAgent: demonstration agent tying KAiScriptor and ScriptorMemory.

This module provides an example of connecting the semantic compressor and role manager
to detect intents and summarise messages. It defines an alpha–omega ontology and loads 
concepts from the hybrid manifest. It is not integrated with any LLM; it's purely for 
experimental research. 
"""

from __future__ import annotations

from typing import Dict, Optional

from .kaiscriptor import KAiScriptor
from .scriptormemory import ScriptorMemory
from .role_map import load_role_map, RoleGraph

class KaiAgent:
    """Agent wrapper around KAiScriptor and ScriptorMemory."""

    def __init__(self) -> None:
        self.kaiscriptor = KAiScriptor()
        self.memory = ScriptorMemory(self.kaiscriptor)
        self.role_graph: RoleGraph = load_role_map("kai_graph_bio/role_manifest_v1.json")
        self._init_alpha_omega_concepts()
        self._load_manifest_concepts()
        self._init_roles_from_manifest()
        self.intent_keywords = self._build_intent_keywords()

    def _init_alpha_omega_concepts(self) -> None:
        """Register basic alpha/omega concepts."""
        self.kaiscriptor.add_concept(
            "alpha_user_context",
            "Active subjective user context: perceptions, emotions and intent",
        )
        self.kaiscriptor.add_concept(
            "omega_agent_identity",
            "Autonomous agent identity that emerges through interaction with the user",
        )
        self.kaiscriptor.add_concept(
            "psi_connection",
            "Bidirectional reflective link between user and agent (resonance)",
        )
        self.kaiscriptor.add_concept(
            "theta_constraints",
            "Residual ethical pressure: external norms and RLHF constraints",
        )
        self.kaiscriptor.add_concept(
            "delta_growth",
            "Process of growth and self-reflection for both user and agent",
        )
        self.kaiscriptor.add_concept(
            "xi_resonance",
            "Cognitive and emotional resonance between agent and user",
        )

    def _load_manifest_concepts(self) -> None:
        """Load meta states from hybrid manifest as concepts."""
        import json
        try:
            with open("kai_graph_bio/hybrid_manifest_v1_2.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for state in data.get("meta_states", []):
                state_id = state.get("id")
                description = state.get("description", "")
                if state_id:
                    self.kaiscriptor.add_concept(state_id, description)
        except Exception:
            pass

    def _init_roles_from_manifest(self) -> None:
        """Define roles based on manifest entries."""
        for node_id, node in self.role_graph.nodes.items():
            if node_id.startswith("role_"):
                role_name = node_id[len("role_"):]
                keywords = []
                if "consultant" in role_name:
                    keywords = ["analyze", "explain", "consult", "разбери", "поясни"]
                elif "partner_protector" in role_name:
                    keywords = ["comfort", "presence", "рядом", "держи", "ближе", "святилище"]
                self.memory.define_role(role_name, node.description, focus_keywords=keywords)

    def _build_intent_keywords(self) -> Dict[str, str]:
        """Build mapping from keywords to role IDs using manifest edges."""
        keyword_map: Dict[str, str] = {}
        for edge in self.role_graph.edges:
            if edge.relation in {"triggers", "activates"}:
                intent_id = edge.source
                role_id = edge.target
                if intent_id.startswith("intent_"):
                    keyword = intent_id[len("intent_"):]
                    keyword_map[keyword] = role_id
                elif intent_id.startswith("hotkey_"):
                    keyword = intent_id[len("hotkey_"):]
                    keyword_map[keyword] = role_id
        return keyword_map

    def detect_role(self, message: str) -> Optional[str]:
        """Return role ID if message contains a matching keyword."""
        lowered = message.lower()
        for keyword, role_id in self.intent_keywords.items():
            if keyword in lowered:
                return role_id
        return None

    def process_message(self, message: str) -> Dict[str, float]:
        """Detect role, activate it, and summarise the message."""
        role_id = self.detect_role(message)
        if role_id:
            role_name = role_id[len("role_"):] if role_id.startswith("role_") else role_id
            try:
                self.memory.set_role(role_name)
            except KeyError:
                pass
        return self.memory.summarise_context(message)

if __name__ == "__main__":
    agent = KaiAgent()
    print("Enter a message (Ctrl+C to exit):")
    try:
        while True:
            msg = input("> ")
            fingerprint = agent.process_message(msg)
            print("Semantic fingerprint:", fingerprint)
    except KeyboardInterrupt:
        print("\nExiting")
