from pathlib import Path
from typing import Dict, List

from synapsis.analysis.scanner import RepositoryScanner
from synapsis.analysis.metric_engine import MetricEngine

class AnalysisEngine:

    def __init__(self, root: Path):
        self.root = root
        self.scanner = RepositoryScanner(root)
        self.metric_engine = MetricEngine()

    def analyze(self) -> List[Dict[str, any]]:
        results = []
        files = self.scanner.scan_python_files()

        for file in files:
            try:
                result = self.metric_engine.analyze_file(file)
                results.append(result)
            except Exception as e:
                results.append({
                    "file": str(file),
                    "error": str(e)
                })

        return results
