import ast
from typing import Any, Dict

from synapsis.analysis.astgraph import extract_unit


class ASTAnalyzer:
    """File-level metrics.

    `lines` and `imports` keep their original definitions exactly, so callers
    and stored snapshots that already read them see no change. The remaining
    keys come from the astgraph extractor and are new.
    """

    def analyze(self, source: str) -> Dict[str, Any]:
        tree = ast.parse(source)

        # Unchanged from the original implementation, deliberately: `imports`
        # counts import *statements*, not imported names. astgraph counts
        # names, which differs for `from x import a, b`. Keeping the original
        # arithmetic avoids silently redefining a metric already in snapshots.
        lines = len(source.splitlines())
        imports = sum(
            isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree)
        )

        graph = extract_unit(source, unit="<source>")
        edges = {}
        for edge in graph.edges:
            edges[edge.edge_type] = edges.get(edge.edge_type, 0) + 1
        grades = {}
        for edge in graph.edges:
            grades[edge.grade] = grades.get(edge.grade, 0) + 1

        return {
            "lines": lines,
            "imports": imports,
            # New, from astgraph.
            "imported_names": edges.get("IMPORTS", 0),
            "calls": edges.get("CALL", 0),
            "inherits": edges.get("INHERITS", 0),
            "symbols": sum(
                1 for n in graph.nodes.values()
                if n.node_type in ("class", "function", "async_function",
                                   "method", "async_method")
            ),
            # Share of call/inheritance targets resolved to a definition in
            # this file (A), to an import (B), or not at all (U).
            "resolved_local": grades.get("A", 0),
            "resolved_import": grades.get("B", 0),
            "unresolved": grades.get("U", 0),
        }
