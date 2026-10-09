from synapsis.reporting.base_reporter import BaseReporter
from synapsis.models.report import Report

class AnalysisReporter(BaseReporter):

    def __init__(self, analysis_results):
        self.results = analysis_results

    def generate(self) -> Report:
        sections = {
            "summary": {
                "files_analyzed": len(self.results)
            },
            "details": self.results
        }
        return self._make_report("analysis_report", sections)
