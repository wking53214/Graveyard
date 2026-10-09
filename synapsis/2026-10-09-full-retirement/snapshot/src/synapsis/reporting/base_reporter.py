from abc import ABC, abstractmethod
from datetime import datetime
from synapsis.models.report import Report

class BaseReporter(ABC):

    @abstractmethod
    def generate(self) -> Report:
        pass

    def _make_report(self, name: str, sections: dict) -> Report:
        return Report(
            name=name,
            created_at=datetime.now(),
            sections=sections
        )
