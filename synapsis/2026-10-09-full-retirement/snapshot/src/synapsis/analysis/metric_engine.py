import ast
from pathlib import Path
from typing import Dict

from synapsis.analysis.ast_analyzer import ASTAnalyzer
from synapsis.analysis.symbol_extractor import SymbolExtractor

class MetricEngine:

    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()
        self.symbol_extractor = SymbolExtractor()

    def analyze_file(self, path: Path) -> Dict[str, any]:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        metrics = self.ast_analyzer.analyze(source)
        symbols = self.symbol_extractor.extract(tree)

        return {
            "file": str(path),
            "metrics": metrics,
            "symbols": symbols
        }
