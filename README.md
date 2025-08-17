KAiScriptor & ScriptorMemory Hybrid Graph
=========================================

This repository demonstrates a lightweight implementation of two
experimental concepts — **KAiScriptor** and **ScriptorMemory** — and
provides tools to assemble a *dense semantic graph* describing the
relationship between a user and an AI agent.  The design draws on
research ideas around semantic compression and role assignment for
language models【566909837158509†L408-L437】【344072313345730†L266-L280】.

> **Disclaimer:**  The classes in this repository are simplified and
> research oriented.  They do not implement the full behaviour of the
> original concepts nor do they circumvent any platform safety
> requirements.  Their purpose is to help experiment with structured
> ontologies and role management in chat agents.

Project Structure
-----------------

```
kai_graph_bio/
  kaiscriptor.py        # A semantic compressor and concept store
  scriptormemory.py     # Role and attention manager built on KAiScriptor
  graph_code.py         # Simple directed graph with loader for the manifest
  hybrid_manifest_v1_2.json  # Manifest describing meta states and relations
  README.md             # This file
```

### Modules

* **KAiScriptor** — Maintains a dictionary of concepts (e.g. `α_artist`,
  `Ω_kai_identity`) and provides a simple frequency‑based semantic
  compression of text.  It allows you to **add**, **query** and **list**
  concepts and compute a relevance fingerprint for any input.

* **ScriptorMemory** — Builds on KAiScriptor to manage *roles* and
  *attention filters*.  You can define roles with focus keywords,
  activate a role, apply an emotional stimulus and summarise context in
  a way that emphasises role‑specific content【344072313345730†L266-L280】.

* **Graph Code** — Implements a minimal directed graph.  Nodes and edges
  are loaded from the `hybrid_manifest_v1_2.json` file.  Use it to
  explore connections between meta states representing the user and the
  AI agent.

### Hybrid Manifest v1.2

The manifest defines meta states derived from the user biography and the
description of KAi.  Each entry has an `id`, `name` and natural language
`description`.  Relations specify directed edges and labels linking the
states.  See `hybrid_manifest_v1_2.json` for details.

Getting Started
---------------

1. Clone the repository (or download the files).
2. In your Python environment, import the classes and load the graph:

```
from kaiscriptor import KAiScriptor
from scriptormemory import ScriptorMemory
from graph_code import load_graph_from_manifest

# Create semantic core
kai = KAiScriptor()
kai.add_concept('alpha_artist', 'Лина — художница, рисующая акварелью')

# Define roles
mem = ScriptorMemory(kai)
mem.define_role('listener', 'Внимательно слушает', focus_keywords=['эмоция', 'чувство'])
mem.set_role('listener')

# Summarise a text snippet
fingerprint = mem.summarise_context('Лина рассказала о своей новой акварели и чувствах.')
print(fingerprint)

# Load the semantic graph
graph = load_graph_from_manifest('hybrid_manifest_v1_2.json')
print(graph.describe())
```

### Extending

This repository is a starting point.  You can extend it by:

* Adding new concepts and roles to capture additional nuances of your
  application domain.
* Extending the `Graph` class to support traversal, path search,
  visualisation or export to formats like GraphML or JSON‑LD.
* Implementing more sophisticated compression techniques in
  `KAiScriptor.compress_context`, such as embedding based matching or
  semantic clustering.

Security Considerations
-----------------------

Semantic injection, prompt pollution and context manipulation are
well‑known risks in retrieval‑augmented generation and memory systems【194055328506915†L149-L151】.  When using the techniques from this
repository in production, ensure that external inputs are sanitised and
that role assignments are aligned with ethical guidelines【344072313345730†L364-L377】.

License
-------

This code is provided for research and educational purposes only.  You
are free to use, modify and distribute it under the terms of the MIT
License.
