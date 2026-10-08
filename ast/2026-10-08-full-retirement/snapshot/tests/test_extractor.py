"""Tests for the structural graph extractor.

The cases that matter most are the resolution ones: `self`, forward
references, and import aliases. Those are the three places where a naive
extractor silently produces a wrong graph rather than an obviously broken one.
"""

import ast
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from astgraph.extractor import extract_unit
from astgraph.model import GRADES, NODE_TYPES


def calls(graph):
    """(source, target, grade) for every CALL edge, unit prefix stripped."""
    return {
        (e.source.split("::", 1)[1], e.target.split("::", 1)[1], e.grade)
        for e in graph.edges
        if e.edge_type == "CALL"
    }


def edges_of(graph, edge_type):
    return {
        (e.source.split("::", 1)[1], e.target.split("::", 1)[1], e.grade)
        for e in graph.edges
        if e.edge_type == edge_type
    }


class TestSelfResolution(unittest.TestCase):
    def test_self_resolves_to_enclosing_class(self):
        graph = extract_unit(
            "class A:\n"
            "    def helper(self): return 1\n"
            "    def run(self): self.helper()\n"
        )
        self.assertIn(("A.run", "A.helper", "A"), calls(graph))

    def test_same_method_name_in_two_classes_stays_distinct(self):
        """The single most important case for a deduplication corpus."""
        graph = extract_unit(
            "class A:\n"
            "    def helper(self): return 1\n"
            "    def run(self): self.helper()\n"
            "class B:\n"
            "    def helper(self): return 2\n"
            "    def run(self): self.helper()\n"
        )
        found = calls(graph)
        self.assertIn(("A.run", "A.helper", "A"), found)
        self.assertIn(("B.run", "B.helper", "A"), found)
        # And crucially: no edge to the bare literal "self.helper"
        self.assertFalse(any(t == "self.helper" for _, t, _ in found))

    def test_cls_resolves_like_self(self):
        graph = extract_unit(
            "class A:\n"
            "    @classmethod\n"
            "    def build(cls): return cls.make()\n"
            "    @classmethod\n"
            "    def make(cls): return 1\n"
        )
        self.assertIn(("A.build", "A.make", "A"), calls(graph))

    def test_self_outside_class_is_unresolved_not_invented(self):
        graph = extract_unit("def loose(self):\n    self.helper()\n")
        self.assertIn(("loose", "self.helper", "U"), calls(graph))

    def test_inherited_method_named_but_graded_unresolved(self):
        """`self.inherited()` with no local definition: name it, do not claim it."""
        graph = extract_unit(
            "class Child(Base):\n"
            "    def run(self): self.inherited()\n"
        )
        self.assertIn(("Child.run", "Child.inherited", "U"), calls(graph))

    def test_super_call_is_marked_unresolved(self):
        graph = extract_unit(
            "class Child(Base):\n"
            "    def run(self): super().run()\n"
        )
        self.assertIn(("Child.run", "<super>.run", "U"), calls(graph))


class TestForwardReferences(unittest.TestCase):
    def test_method_may_call_helper_defined_below_it(self):
        """Resolution runs after the walk, so source order does not matter."""
        graph = extract_unit(
            "class A:\n"
            "    def run(self): self.helper()\n"
            "    def helper(self): return 1\n"
        )
        self.assertIn(("A.run", "A.helper", "A"), calls(graph))

    def test_function_may_use_import_declared_below_it(self):
        graph = extract_unit(
            "def run(): return np.array([])\n"
            "import numpy as np\n"
        )
        self.assertIn(("run", "numpy.array", "B"), calls(graph))


class TestImports(unittest.TestCase):
    def test_aliased_import_resolves_to_real_module(self):
        graph = extract_unit("import numpy as np\ndef f(): return np.array([])\n")
        self.assertIn(("f", "numpy.array", "B"), calls(graph))

    def test_from_import_resolves_to_dotted_path(self):
        graph = extract_unit(
            "from os.path import join\ndef f(): return join('a', 'b')\n"
        )
        self.assertIn(("f", "os.path.join", "B"), calls(graph))

    def test_from_import_with_alias(self):
        graph = extract_unit(
            "from os.path import join as j\ndef f(): return j('a')\n"
        )
        self.assertIn(("f", "os.path.join", "B"), calls(graph))

    def test_imports_edges_recorded_from_module(self):
        graph = extract_unit("import hashlib\nfrom typing import Dict\n")
        found = edges_of(graph, "IMPORTS")
        self.assertIn(("<module>", "hashlib", "B"), found)
        self.assertIn(("<module>", "typing.Dict", "B"), found)


class TestInheritance(unittest.TestCase):
    def test_local_base_resolves_grade_a(self):
        graph = extract_unit("class Base: pass\nclass Child(Base): pass\n")
        self.assertIn(("Child", "Base", "A"), edges_of(graph, "INHERITS"))

    def test_imported_base_resolves_grade_b(self):
        graph = extract_unit("import ast\nclass V(ast.NodeVisitor): pass\n")
        self.assertIn(("V", "ast.NodeVisitor", "B"), edges_of(graph, "INHERITS"))

    def test_unknown_base_graded_unresolved(self):
        graph = extract_unit("class Child(Mystery): pass\n")
        self.assertIn(("Child", "Mystery", "U"), edges_of(graph, "INHERITS"))


class TestContainment(unittest.TestCase):
    def test_module_contains_class_contains_method(self):
        graph = extract_unit("class A:\n    def m(self): pass\n")
        found = edges_of(graph, "CONTAINS")
        self.assertIn(("<module>", "A", "A"), found)
        self.assertIn(("A", "A.m", "A"), found)

    def test_nested_function_qualnames(self):
        graph = extract_unit("def outer():\n    def inner(): pass\n    inner()\n")
        self.assertIn(("outer", "outer.inner", "A"), edges_of(graph, "CONTAINS"))
        self.assertIn(("outer", "outer.inner", "A"), calls(graph))

    def test_method_and_function_node_types_differ(self):
        graph = extract_unit("def f(): pass\nclass A:\n    def m(self): pass\n")
        types = {n.name: n.node_type for n in graph.nodes.values()}
        self.assertEqual(types["f"], "function")
        self.assertEqual(types["A.m"], "method")

    def test_async_types(self):
        graph = extract_unit(
            "async def f(): pass\nclass A:\n    async def m(self): pass\n"
        )
        types = {n.name: n.node_type for n in graph.nodes.values()}
        self.assertEqual(types["f"], "async_function")
        self.assertEqual(types["A.m"], "async_method")


class TestGraphClosure(unittest.TestCase):
    def test_every_edge_endpoint_exists_as_a_node(self):
        """The bug in the original: edges pointing at names with no node."""
        source = (
            "import math\n"
            "class A(Base):\n"
            "    def run(self):\n"
            "        self.helper()\n"
            "        math.sqrt(1)\n"
            "        unknown_thing()\n"
            "    def helper(self): pass\n"
        )
        graph = extract_unit(source)
        ids = set(graph.nodes)
        for edge in graph.edges:
            self.assertIn(edge.source, ids, f"dangling source: {edge.source}")
            self.assertIn(edge.target, ids, f"dangling target: {edge.target}")

    def test_unresolved_targets_registered_as_external(self):
        graph = extract_unit("def f(): unknown_thing()\n")
        types = {n.name: n.node_type for n in graph.nodes.values()}
        self.assertEqual(types["unknown_thing"], "external")


class TestBuiltins(unittest.TestCase):
    def test_builtins_excluded_by_default(self):
        graph = extract_unit("def f(): print(len('x'))\n")
        targets = {t for _, t, _ in calls(graph)}
        self.assertNotIn("builtins.print", targets)
        self.assertNotIn("print", targets)

    def test_builtins_included_on_request(self):
        graph = extract_unit("def f(): print('x')\n", include_builtins=True)
        self.assertIn(("f", "builtins.print", "B"), calls(graph))

    def test_local_definition_shadows_builtin(self):
        graph = extract_unit("def list(): pass\ndef f(): list()\n")
        self.assertIn(("f", "list", "A"), calls(graph))


class TestParseFailures(unittest.TestCase):
    def test_syntax_error_recorded_not_raised(self):
        graph = extract_unit("def broken(:\n", unit="U1")
        self.assertEqual(len(graph.failures), 1)
        self.assertEqual(graph.nodes, {})
        failure = graph.failures[0]
        self.assertEqual(failure.unit, "U1")
        self.assertEqual(failure.error_type, "SyntaxError")
        self.assertTrue(failure.source_sha256)

    def test_null_byte_recorded_not_raised(self):
        """Which exception type CPython picks here varies by version.

        What must hold is that it is caught and recorded rather than escaping
        and killing a corpus run partway through.
        """
        graph = extract_unit("x = 1\x00\n", unit="U2")
        self.assertEqual(len(graph.failures), 1)
        self.assertEqual(graph.failures[0].unit, "U2")
        self.assertIn(graph.failures[0].error_type, {"ValueError", "SyntaxError"})

    def test_row_numbered_output_from_the_transcript_fails_cleanly(self):
        """The [Row ###] prefixed code is a syntax error, and must be logged."""
        graph = extract_unit("[Row 015] import ast\n[Row 016] class A: pass\n")
        self.assertEqual(len(graph.failures), 1)


class TestDeterminism(unittest.TestCase):
    def test_identical_input_yields_identical_edge_ids(self):
        source = "class A:\n    def m(self): self.n()\n    def n(self): pass\n"
        first = extract_unit(source, unit="X")
        second = extract_unit(source, unit="X")
        self.assertEqual(
            [e.edge_id for e in first.sorted_edges()],
            [e.edge_id for e in second.sorted_edges()],
        )

    def test_sort_order_is_stable(self):
        source = "class B:\n    def z(self): pass\nclass A:\n    def a(self): pass\n"
        graph = extract_unit(source, unit="X")
        names = [n.node_id for n in graph.sorted_nodes()]
        self.assertEqual(names, sorted(names))


class TestVocabularies(unittest.TestCase):
    def test_all_emitted_types_are_declared(self):
        graph = extract_unit(
            "import os\n"
            "class Base: pass\n"
            "class A(Base):\n"
            "    async def m(self):\n"
            "        self.n()\n"
            "        os.getcwd()\n"
            "    def n(self): pass\n"
            "def top(): pass\n"
        )
        for node in graph.nodes.values():
            self.assertIn(node.node_type, NODE_TYPES)
        for edge in graph.edges:
            self.assertIn(edge.grade, GRADES)


class TestSelfConsistency(unittest.TestCase):
    def test_extractor_can_parse_its_own_source(self):
        """The tool must handle the most realistic file available: itself."""
        root = Path(__file__).resolve().parents[1] / "astgraph"
        for path in sorted(root.glob("*.py")):
            graph = extract_unit(path.read_text(), unit=path.name)
            self.assertEqual(graph.failures, [], f"{path.name} failed to parse")
            ids = set(graph.nodes)
            for edge in graph.edges:
                self.assertIn(edge.target, ids)

    def test_finds_known_structure_in_its_own_extractor(self):
        path = Path(__file__).resolve().parents[1] / "astgraph" / "extractor.py"
        graph = extract_unit(path.read_text(), unit="extractor.py")
        names = {n.name for n in graph.nodes.values()}
        self.assertIn("GraphExtractor", names)
        self.assertIn("GraphExtractor.visit_ClassDef", names)
        # ast.NodeVisitor inheritance, resolved through the `import ast` binding
        self.assertIn(
            ("GraphExtractor", "ast.NodeVisitor", "B"), edges_of(graph, "INHERITS")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
