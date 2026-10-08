"""Deterministic structural graph extraction from Python source.

What this does
--------------
Parses a unit of Python source and emits the symbols it defines (classes,
functions, methods) plus the relationships between them (calls, containment,
inheritance, imports).

What this deliberately does not do
----------------------------------
No type inference, no cross-module import following, no execution. Every
resolution is derived from the syntax of the unit alone. When a target cannot
be resolved from syntax, the edge is still recorded but graded ``U`` rather
than guessed at. An honest unresolved edge is more useful than a confident
wrong one.

The two-pass shape
------------------
Definitions and imports are collected during the walk, but call targets are
resolved *after* the walk completes. This matters because Python does not
require a name to be defined before the line that references it: a method can
call a helper defined below it, and an import can appear after a function that
uses it. Resolving during the walk would mis-grade those as unresolved.
"""

from __future__ import annotations

import ast
import builtins
import hashlib
from typing import Dict, List, Optional, Tuple

from .model import Edge, Graph, Node, ParseFailure

_BUILTINS = frozenset(dir(builtins))

# Roots of an attribute chain that refer to the enclosing class instance.
_SELF_NAMES = frozenset({"self", "cls"})

SNIPPET_LIMIT = 400  # characters of source kept on a parse failure


class _Pending:
    """A call site recorded during the walk, resolved after it."""

    __slots__ = ("caller", "enclosing_class", "func", "lineno", "evidence")

    def __init__(self, caller: str, enclosing_class: Optional[str], func: ast.AST,
                 lineno: int, evidence: str) -> None:
        self.caller = caller
        self.enclosing_class = enclosing_class
        self.func = func
        self.lineno = lineno
        self.evidence = evidence


class GraphExtractor(ast.NodeVisitor):
    """Walks one parsed unit and builds its structural graph."""

    def __init__(self, unit: str = "<unit>", include_builtins: bool = False) -> None:
        self.unit = unit
        self.include_builtins = include_builtins

        # Scope stack of (name, kind) frames. Drives qualified naming and is
        # how we find the class a `self.` reference belongs to.
        self._scope: List[Tuple[str, str]] = []

        self._defined: Dict[str, str] = {}      # qualname -> node_type
        self._aliases: Dict[str, str] = {}      # local binding -> dotted target
        self._pending: List[_Pending] = []      # call sites awaiting resolution
        self._inherits: List[Tuple[str, ast.AST, int]] = []  # class, base, lineno

        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    # -- naming helpers -----------------------------------------------------

    @property
    def _scope_names(self) -> List[str]:
        return [name for name, _ in self._scope]

    def _qualname(self, name: str) -> str:
        """Fully qualified name of `name` as defined at the current scope."""
        return ".".join(self._scope_names + [name]) if self._scope else name

    def _current_qual(self) -> str:
        """Qualified name of the scope we are currently inside."""
        return ".".join(self._scope_names) if self._scope else "<module>"

    def _enclosing_class(self) -> Optional[str]:
        """Qualified name of the nearest enclosing class, if any.

        This is what makes `self.helper()` resolvable. Without it every
        `self.` call in the corpus collapses to the literal string
        "self.helper", which is neither a real symbol nor distinguishable
        between two classes that both define `helper`.
        """
        for index in range(len(self._scope) - 1, -1, -1):
            if self._scope[index][1] == "class":
                return ".".join(self._scope_names[: index + 1])
        return None

    def _node_id(self, qualname: str) -> str:
        """Namespace a qualified name to its unit.

        Units are namespaced so two unrelated blocks that both define `Engine`
        stay distinct nodes. The unqualified `name` field is preserved on each
        node so a later pass can group identical structures across units.
        """
        return f"{self.unit}::{qualname}"

    def _add_node(self, qualname: str, node_type: str, lineno: int = 0) -> str:
        node_id = self._node_id(qualname)
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                node_id=node_id,
                node_type=node_type,
                name=qualname,
                unit=self.unit,
                lineno=lineno,
            )
        return node_id

    def _add_edge(self, source_qual: str, target_qual: str, edge_type: str,
                  grade: str, lineno: int = 0, evidence: str = "") -> None:
        self.edges.append(
            Edge.make(
                source=self._node_id(source_qual),
                target=self._node_id(target_qual),
                edge_type=edge_type,
                grade=grade,
                unit=self.unit,
                lineno=lineno,
                evidence=evidence,
            )
        )

    # -- definition visiting ------------------------------------------------

    def visit_Module(self, node: ast.Module) -> None:
        self._add_node("<module>", "module", 0)
        self._defined["<module>"] = "module"
        self.generic_visit(node)

    def _visit_def(self, node: ast.AST, is_async: bool) -> None:
        """Shared handling for sync and async function/method definitions."""
        qualname = self._qualname(node.name)
        inside_class = bool(self._scope) and self._scope[-1][1] == "class"
        if inside_class:
            node_type = "async_method" if is_async else "method"
        else:
            node_type = "async_function" if is_async else "function"

        self._add_node(qualname, node_type, node.lineno)
        self._defined[qualname] = node_type
        self._add_edge(self._current_qual(), qualname, "CONTAINS", "A", node.lineno)

        self._scope.append((node.name, "function"))
        self.generic_visit(node)
        self._scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_def(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_def(node, is_async=True)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        qualname = self._qualname(node.name)
        self._add_node(qualname, "class", node.lineno)
        self._defined[qualname] = "class"
        self._add_edge(self._current_qual(), qualname, "CONTAINS", "A", node.lineno)

        # Base classes are resolved after the walk, same as call targets.
        for base in node.bases:
            self._inherits.append((qualname, base, node.lineno))

        self._scope.append((node.name, "class"))
        self.generic_visit(node)
        self._scope.pop()

    # -- imports ------------------------------------------------------------

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            target = alias.name
            binding = alias.asname or alias.name.split(".")[0]
            # `import os.path` binds `os`, but the dotted module is what the
            # code will actually reference, so record the full path as a node.
            self._aliases[binding] = alias.asname and target or target.split(".")[0]
            if alias.asname:
                self._aliases[binding] = target
            self._add_node(target, "import", node.lineno)
            self._add_edge("<module>", target, "IMPORTS", "B", node.lineno,
                           evidence=f"import {target}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            full = f"{module}.{alias.name}" if module else alias.name
            binding = alias.asname or alias.name
            self._aliases[binding] = full
            self._add_node(full, "import", node.lineno)
            self._add_edge("<module>", full, "IMPORTS", "B", node.lineno,
                           evidence=f"from {module} import {alias.name}")
        self.generic_visit(node)

    # -- call sites ---------------------------------------------------------

    def visit_Call(self, node: ast.Call) -> None:
        try:
            evidence = ast.unparse(node)
        except Exception:  # pragma: no cover - unparse is total on parsed trees
            evidence = ""
        self._pending.append(
            _Pending(
                caller=self._current_qual(),
                enclosing_class=self._enclosing_class(),
                func=node.func,
                lineno=getattr(node, "lineno", 0),
                evidence=evidence,
            )
        )
        self.generic_visit(node)

    # -- resolution (runs after the walk) -----------------------------------

    def _resolve_local(self, name: str) -> Optional[str]:
        """Find `name` as a definition visible from the current scope.

        Walks outward from the innermost scope so a nested helper shadows a
        module-level one of the same name, matching Python's own lookup order
        closely enough for structural purposes.
        """
        names = self._scope_names
        for index in range(len(names), -1, -1):
            prefix = ".".join(names[:index])
            candidate = f"{prefix}.{name}" if prefix else name
            if candidate in self._defined:
                return candidate
        return None

    def _attr_chain(self, node: ast.Attribute) -> Tuple[Optional[ast.AST], List[str]]:
        """Flatten `a.b.c` into (root_node, ['b', 'c'])."""
        parts: List[str] = []
        current: ast.AST = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        parts.reverse()
        return current, parts

    def _resolve_target(self, func: ast.AST, enclosing_class: Optional[str],
                        scope_at_call: List[str]) -> Tuple[Optional[str], str]:
        """Resolve a call target to (qualname, grade).

        Returns (None, 'U') when the call should be dropped entirely, which
        currently only happens for builtins when they are not being recorded.
        """
        # foo()
        if isinstance(func, ast.Name):
            local = self._resolve_scoped(func.id, scope_at_call)
            if local:
                return local, "A"
            if func.id in self._aliases:
                return self._aliases[func.id], "B"
            if func.id in _BUILTINS:
                if not self.include_builtins:
                    return None, "U"
                return f"builtins.{func.id}", "B"
            return func.id, "U"

        # a.b.c()
        if isinstance(func, ast.Attribute):
            root, parts = self._attr_chain(func)
            dotted = ".".join(parts)

            # super().method()
            if isinstance(root, ast.Call) and isinstance(root.func, ast.Name) \
                    and root.func.id == "super":
                return f"<super>.{dotted}", "U"

            if not isinstance(root, ast.Name):
                return "<dynamic>", "U"

            # self.method() / cls.method()  -- the resolution that matters most
            if root.id in _SELF_NAMES:
                if enclosing_class is None:
                    return f"{root.id}.{dotted}", "U"
                candidate = f"{enclosing_class}.{dotted}"
                if candidate in self._defined:
                    return candidate, "A"
                # Named against the right class, but not defined here. Most
                # likely inherited from a base outside this unit, so the name
                # is reported and the grade stays unresolved.
                return candidate, "U"

            # numpy.array() where `import numpy as np` was seen
            if root.id in self._aliases:
                return f"{self._aliases[root.id]}.{dotted}", "B"

            # ClassName.method() for a class defined in this unit
            local_root = self._resolve_scoped(root.id, scope_at_call)
            if local_root:
                candidate = f"{local_root}.{dotted}"
                if candidate in self._defined:
                    return candidate, "A"
                return candidate, "U"

            return f"{root.id}.{dotted}", "U"

        # Anything else: a lambda call, a subscripted callable, a call on a
        # call. Recorded so the undecidable share of the graph is visible.
        return "<dynamic>", "U"

    def _resolve_scoped(self, name: str, scope_names: List[str]) -> Optional[str]:
        for index in range(len(scope_names), -1, -1):
            prefix = ".".join(scope_names[:index])
            candidate = f"{prefix}.{name}" if prefix else name
            if candidate in self._defined:
                return candidate
        return None

    def finalize(self) -> None:
        """Resolve pending calls and inheritance, then close the graph.

        Closing the graph means every edge target is guaranteed to exist as a
        node. Targets that were never defined in this unit are registered as
        ``external`` so nothing dangles.
        """
        for pending in self._pending:
            scope_at_call = pending.caller.split(".") if pending.caller != "<module>" else []
            target, grade = self._resolve_target(
                pending.func, pending.enclosing_class, scope_at_call
            )
            if target is None:
                continue
            self._register_target(target)
            self._add_edge(pending.caller, target, "CALL", grade,
                           pending.lineno, pending.evidence)

        for class_qual, base, lineno in self._inherits:
            scope_at_call = class_qual.split(".")[:-1]
            target, grade = self._resolve_target(base, None, scope_at_call)
            if target is None:
                continue
            self._register_target(target)
            try:
                evidence = ast.unparse(base)
            except Exception:  # pragma: no cover
                evidence = ""
            self._add_edge(class_qual, target, "INHERITS", grade, lineno, evidence)

    def _register_target(self, qualname: str) -> None:
        """Ensure an edge target exists as a node.

        Without this the graph has edges pointing at names that are not in the
        node table, which makes it unusable for any graph algorithm and hides
        how much of the call surface is external.
        """
        node_id = self._node_id(qualname)
        if node_id in self.nodes:
            return
        node_type = self._defined.get(qualname, "external")
        self._add_node(qualname, node_type if node_type in {"class", "function",
                                                            "async_function", "method",
                                                            "async_method", "module"}
                       else "external")


def extract_unit(source: str, unit: str = "<unit>",
                 include_builtins: bool = False) -> Graph:
    """Extract one unit of source into a Graph.

    A syntax error is not an exception here: it is recorded as a ParseFailure
    and returned in an otherwise empty graph, so a caller iterating a corpus
    never has to choose between crashing and silently dropping a row.
    """
    graph = Graph()
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        graph.failures.append(
            ParseFailure(
                unit=unit,
                error_type=type(exc).__name__,
                message=str(exc.msg),
                lineno=exc.lineno or 0,
                offset=exc.offset or 0,
                source_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
                snippet=source[:SNIPPET_LIMIT],
            )
        )
        return graph
    except (ValueError, RecursionError, MemoryError) as exc:
        # Null bytes, absurd nesting depth, and pathological inputs reach here.
        graph.failures.append(
            ParseFailure(
                unit=unit,
                error_type=type(exc).__name__,
                message=str(exc),
                source_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
                snippet=source[:SNIPPET_LIMIT],
            )
        )
        return graph

    extractor = GraphExtractor(unit=unit, include_builtins=include_builtins)
    extractor.visit(tree)
    extractor.finalize()
    graph.nodes = extractor.nodes
    graph.edges = extractor.edges
    return graph
