from pathlib import Path
from datetime import datetime

from synapsis.analysis.analysis_engine import AnalysisEngine
from synapsis.reporting.analysis_reporter import AnalysisReporter
from synapsis.memory.analysis_memory import AnalysisMemory
from synapsis.memory.snapshot_memory import SnapshotMemory
from synapsis.models.snapshot import Snapshot

class IntelligenceEngine:

    def __init__(self, root: Path):
        self.root = root
        self.analysis_engine = AnalysisEngine(root)
        self.analysis_memory = AnalysisMemory()
        self.snapshot_memory = SnapshotMemory()

    def run_full_analysis(self):
        # Run analysis
        results = self.analysis_engine.analyze()

        # Save analysis memory
        self.analysis_memory.save_analysis(results)

        # Generate report
        report = AnalysisReporter(results).generate()

        # Save snapshot
        snapshot = Snapshot(
            name=f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            created_at=datetime.now(),
            data=report.sections
        )
        self.snapshot_memory.save_snapshot(snapshot)

        return {
            "analysis_results": results,
            "report": report,
            "snapshot": snapshot
        }
