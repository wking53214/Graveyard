from pathlib import Path
from synapsis.intelligence.intelligence_engine import IntelligenceEngine

class IntelligenceAPI:

    def __init__(self, root: Path):
        self.engine = IntelligenceEngine(root)

    def analyze_project(self):
        return self.engine.run_full_analysis()
