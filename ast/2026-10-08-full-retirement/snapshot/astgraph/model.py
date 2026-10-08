"""Data model for the structural graph.

Three record types come out of an extraction run:

* ``Node``          -- a symbol (module, class, function, method, import, external)
* ``Edge``          -- a relationship between two symbols
* ``ParseFailure``  -- a unit that could not be parsed at all

Every record is a frozen dataclass so a graph cannot be mutated after it is
built, and every record serialises to a flat JSON object so the output files
are plain JSONL that any tool can read.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Dict, List

# ---------------------------------------------------------------------------
# Vocabularies. Kept as plain frozensets so they can be asserted against in
# tests and referenced in documentation without importing an enum.
# ---------------------------------------------------------------------------

NODE_TYPES = frozenset(
    {
        "module",
        "class",
        "function",
        "async_function",
        "method",
        "async_method",
        "import",
        "external",
    }
)

EDGE_TYPES = frozenset({"CALL", "CONTAINS", "INHERITS", "IMPORTS"})

# Evidence grades, matching the A/B/C/U vocabulary used by the consuming
# forensic repositories.
#
#   A -- target is defined inside the same unit. Fully resolved, and the
#        resolution can be re-derived from the unit alone.
#   B -- target resolved through an import binding to a module-qualified
#        name. The name is known; the definition lives outside this unit.
#   U -- target could not be resolved (dynamic dispatch, ``super()``, an
#        attribute chain rooted in an unknown object).
#
# There is deliberately no C. A structural edge is either resolved locally,
# resolved to an import, or unresolved. Nothing in between is decidable
# without type inference, which this extractor does not attempt.
GRADES = frozenset({"A", "B", "U"})

EVIDENCE_LIMIT = 300  # characters of source kept per edge


def _digest(*parts: object) -> str:
    """Short, stable content hash used to build record IDs.

    Deterministic across runs and machines: the same input always yields the
    same ID, so re-running an extraction produces a byte-identical file and
    ``git diff`` shows only real changes.
    """
    joined = "\x1f".join(str(p) for p in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class Node:
    """A symbol in the graph."""

    node_id: str
    node_type: str
    name: str
    unit: str
    lineno: int = 0

    def __post_init__(self) -> None:
        if self.node_type not in NODE_TYPES:
            raise ValueError(f"unknown node_type: {self.node_type!r}")


@dataclass(frozen=True)
class Edge:
    """A relationship between two symbols."""

    edge_id: str
    source: str
    target: str
    edge_type: str
    grade: str
    unit: str
    lineno: int = 0
    evidence: str = ""

    def __post_init__(self) -> None:
        if self.edge_type not in EDGE_TYPES:
            raise ValueError(f"unknown edge_type: {self.edge_type!r}")
        if self.grade not in GRADES:
            raise ValueError(f"unknown grade: {self.grade!r}")

    @staticmethod
    def make(
        source: str,
        target: str,
        edge_type: str,
        grade: str,
        unit: str,
        lineno: int = 0,
        evidence: str = "",
    ) -> "Edge":
        """Build an Edge with a deterministic ID derived from its content."""
        evidence = evidence[:EVIDENCE_LIMIT]
        return Edge(
            edge_id=f"E-{_digest(unit, source, target, edge_type, lineno)}",
            source=source,
            target=target,
            edge_type=edge_type,
            grade=grade,
            unit=unit,
            lineno=lineno,
            evidence=evidence,
        )


@dataclass(frozen=True)
class ParseFailure:
    """A unit that could not be parsed.

    This is a first-class output, not a skipped row. In a corpus of generated
    code, "this artifact never compiled" is itself a finding worth recording.
    """

    unit: str
    error_type: str
    message: str
    lineno: int = 0
    offset: int = 0
    source_sha256: str = ""
    snippet: str = ""


@dataclass
class Graph:
    """The result of an extraction run."""

    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    failures: List[ParseFailure] = field(default_factory=list)

    def merge(self, other: "Graph") -> None:
        """Fold another graph into this one.

        Node IDs are namespaced by unit, so collisions across units are not
        expected; if one occurs the first definition wins and the second is
        discarded rather than silently overwriting it.
        """
        for node_id, node in other.nodes.items():
            self.nodes.setdefault(node_id, node)
        self.edges.extend(other.edges)
        self.failures.extend(other.failures)

    def sorted_nodes(self) -> List[Node]:
        return sorted(self.nodes.values(), key=lambda n: (n.unit, n.node_id))

    def sorted_edges(self) -> List[Edge]:
        return sorted(
            self.edges,
            key=lambda e: (e.unit, e.source, e.edge_type, e.target, e.lineno),
        )

    def summary(self) -> Dict[str, int]:
        """Counts used for the run report and for regression assertions."""
        out: Dict[str, int] = {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "parse_failures": len(self.failures),
        }
        for node in self.nodes.values():
            out[f"node_type.{node.node_type}"] = out.get(f"node_type.{node.node_type}", 0) + 1
        for edge in self.edges:
            out[f"edge_type.{edge.edge_type}"] = out.get(f"edge_type.{edge.edge_type}", 0) + 1
            out[f"grade.{edge.grade}"] = out.get(f"grade.{edge.grade}", 0) + 1
        return out


def write_jsonl(path: str, records: List[object]) -> int:
    """Write dataclass records as JSONL. Returns the number of rows written."""
    count = 0
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")
            count += 1
    return count
