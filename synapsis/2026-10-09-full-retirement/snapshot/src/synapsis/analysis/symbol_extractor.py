import ast
from typing import Any, Dict, List

from synapsis.analysis.astgraph import GraphExtractor


class SymbolExtractor:
    """Symbol inventory for one parsed module.

    Backed by the astgraph extractor rather than a bare `ast.walk`. Three
    behaviour changes follow from that, all corrections:

    * `async def` is recognised. The previous implementation matched only
      `ast.FunctionDef`, so every async function and method was invisible.
    * A method appears in `methods` only. The previous implementation used
      `ast.walk`, which descends into class bodies, so every method was also
      listed in `functions`.
    * Names are qualified by their enclosing scope, so a nested class reads
      `Outer.Inner` and a nested function `outer.inner`.
    """

    def extract(self, tree: ast.AST) -> Dict[str, List[str]]:
        extractor = GraphExtractor(unit="<tree>")
        extractor.visit(tree)
        extractor.finalize()

        def names(*kinds: str) -> List[str]:
            return sorted(
                n.name for n in extractor.nodes.values() if n.node_type in kinds
            )

        return {
            "functions": names("function", "async_function"),
            "classes": names("class"),
            "methods": names("method", "async_method"),
            # New: previously indistinguishable from their sync counterparts.
            "async_functions": names("async_function"),
            "async_methods": names("async_method"),
        }
