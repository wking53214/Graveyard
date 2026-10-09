"""
ContentPolishPipeline: LLM output quality gate.

Validates generated text against linguistic constraints (pronouns, speculation,
empirical evidence) and retries generation with recalibration feedback until
output meets standards or max attempts exhausted.

Usage:
    pipeline = ContentPolishPipeline(
        execution_gateway=my_llm_call,
        max_attempts=5
    )
    result = await pipeline.execute("Generate a report on X")
    if result["execution_status"] == "SUCCESS":
        validated_text = result["validated_content"]
"""

from .pipeline import ContentPolishPipeline
from .filters import (
    PersonalPronounFilter,
    SpeculativeLanguageFilter,
    EmpiricalValidationFilter,
)
from .oscillation import OscillationDetector

__version__ = "1.2.0"
__all__ = [
    "ContentPolishPipeline",
    "PersonalPronounFilter",
    "SpeculativeLanguageFilter",
    "EmpiricalValidationFilter",
    "OscillationDetector",
]
