# SYNAPSIS

## **System Intelligence, Archaeology, Memory, and Reconstruction**

### **A Domain-Independent Architecture for Understanding How Complex Systems Exist, Change, Remember, and Evolve**

> **Synapsis is not merely a code-analysis engine. It is an architectural foundation for reconstructing the structure, history, relationships, decisions, state, and accumulated intelligence of a complex system.**

---

# **What Synapsis Is**

Synapsis is a modular architecture for turning a complex software system from something that can merely be **scanned** into something that can be **understood over time**.

The current implementation demonstrates this capability primarily through software repositories.

The repository is therefore the **representative implementation environment**.

The underlying architecture is broader.

Synapsis is concerned with:

- system structure;
- code relationships;
- historical evolution;
- snapshots;
- timelines;
- changes;
- project archaeology;
- knowledge graphs;
- accumulated memory;
- analytical intelligence;
- system health;
- governance observations; and
- reconstruction of how a system arrived at its current state.

The fundamental problem is not:

> **"What is here?"**

It is:

> **"What is here, how did it get here, what changed, what did the system previously know, what relationships exist between its parts, and what can be reconstructed about its evolution?"**

---

# **The Fundamental Architecture**

```text
                    SYSTEM
                       │
                       ▼
                  OBSERVATION
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       STRUCTURE     HISTORY      CONTEXT
          │            │            │
          ▼            ▼            ▼
         AST          DIFFS       ARCHIVES
          │            │            │
          └────────────┼────────────┘
                       ▼
                   KNOWLEDGE
                       │
                       ▼
                     GRAPH
                       │
                       ▼
                    MEMORY
                       │
                       ▼
                   TIMELINE
                       │
                       ▼
                 INTELLIGENCE
                       │
                       ▼
                 RECONSTRUCTION
                       │
                       ▼
                   GOVERNANCE
```

---

# What Is Actually Implemented

The diagram above is the target architecture, not a description of the current codebase. As of this cleanup pass, most of the originally-scaffolded module tree (`archaeology/`, `knowledge/`, `search/`, `restoration/`, `governance/`, `interaction/`, most CLI subcommands) was removed: those modules were 4-line docstring stubs with no logic and zero corresponding tests, left over from a single scaffolding pass and never built out.

What survives and actually runs:

- **`analysis/`** — a real `.gitignore`-aware, recursive Python file scanner (`scanner.py` + `gitignore.py`), plus AST-based line/import counting and function/class/method-name extraction (`ast_analyzer.py`, `symbol_extractor.py`).
- **`intelligence/`** — orchestrates a scan → analyze → report → snapshot pass over a repository.
- **`memory/` + `storage/`** — a flat JSON-file key/value store for saved analysis results and snapshots (no database, no schema versioning, no cross-snapshot linkage).
- **`cli/cli.py`** — the only wired-up entry point: `synapsis analyze`, `synapsis memory {list,load}`, `synapsis snapshot <name>`.

What is not implemented, despite the architecture diagram above: code archaeology, chat-history archaeology, knowledge graphs, timelines, diffing, restoration, search, and governance scorecards. There is currently no test suite for the surviving modules — the prior `tests/` tree was removed along with the stub modules it tested (63 files, all empty).

If you're picking this project back up: treat the diagram as a backlog, not a status report, and write real tests against `analysis/`, `intelligence/`, and `memory/` before extending further.