from synapsis.analysis.ast_analyzer import ASTAnalyzer
from synapsis.analysis.symbol_extractor import SymbolExtractor
import ast

SOURCE = '''
import os
import sys

class Foo:
    def bar(self):
        pass

def baz():
    pass
'''


def test_ast_analyzer_counts_lines_and_imports():
    result = ASTAnalyzer().analyze(SOURCE)
    assert result["imports"] == 2
    assert result["lines"] == SOURCE.count("\n")


def test_symbol_extractor_finds_classes_and_methods():
    tree = ast.parse(SOURCE)
    result = SymbolExtractor().extract(tree)

    assert result["classes"] == ["Foo"]
    assert result["methods"] == ["Foo.bar"]
    assert "baz" in result["functions"]


def test_symbol_extractor_no_longer_leaks_methods_into_functions():
    # Was: extract() used ast.walk(), which descends into class bodies, so a
    # method name landed in `functions` as well as in `methods`. The previous
    # test pinned that as known-wrong and deferred it. The astgraph extractor
    # classifies by enclosing scope, so it is now fixed.
    tree = ast.parse(SOURCE)
    result = SymbolExtractor().extract(tree)

    assert "bar" not in result["functions"]
    assert result["methods"] == ["Foo.bar"]


ASYNC_SOURCE = '''
async def fetch():
    pass

class Client:
    async def get(self):
        pass
'''


def test_symbol_extractor_sees_async_definitions():
    # The previous implementation matched only ast.FunctionDef, so every
    # async def in the corpus was invisible to it.
    result = SymbolExtractor().extract(ast.parse(ASYNC_SOURCE))

    assert result["async_functions"] == ["fetch"]
    assert result["async_methods"] == ["Client.get"]


def test_ast_analyzer_reports_resolution_grades():
    source = "import math\n\nclass A:\n    def run(self):\n        self.helper()\n        math.sqrt(1)\n    def helper(self):\n        pass\n"
    result = ASTAnalyzer().analyze(source)

    assert result["calls"] == 2
    assert result["resolved_local"] >= 1    # self.helper -> A.helper
    assert result["resolved_import"] >= 1   # math.sqrt via the import
