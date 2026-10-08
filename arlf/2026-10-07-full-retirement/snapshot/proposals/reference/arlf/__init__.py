"""Reference implementation for two ARLF proposals.

This package is NEW WORK. It is not a reconstruction of anything in the Gemini
archive, which contains no ARLF implementation of any kind. It exists to make two
proposed fixes demonstrable rather than merely asserted:

  * proposals/AUTHORITY_GAP_RESOLUTION.md  -- ternary resolution with certificates
  * proposals/RLCF_SPECIFICATION.md        -- the Charity Protocol as a ranking signal

Standard library only. No dependencies.
"""

from .resolution import Verdict, Resolution
from .certificate import Cause, Certificate, Escalation
from .substrate import Literal, Rule, Substrate, Discharge
from .gates import AlphaOmegaGates, Admission, Sphere
from .governor import KineticGovernor, BudgetExhausted
from .rlcf import Candidate, Exchange, structural_score, charity_penalty, rlcf_score, rank
from .pipeline import admit, resolve, select

__all__ = [
    "Verdict", "Resolution", "Cause", "Certificate", "Escalation",
    "Literal", "Rule", "Substrate", "Discharge",
    "AlphaOmegaGates", "Admission", "Sphere",
    "KineticGovernor", "BudgetExhausted",
    "Candidate", "Exchange", "structural_score", "charity_penalty", "rlcf_score", "rank",
    "admit", "resolve", "select",
]
