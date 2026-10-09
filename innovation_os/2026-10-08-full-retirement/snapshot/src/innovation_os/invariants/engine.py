from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .models import InvariantViolation
from ..provenance.status import ProvenanceStatus


class InvariantEngine:

    def __init__(self):
        self.violations = []

    def _record_violation(
        self,
        subject_type: str,
        subject_id: str,
        rule_name: str,
        context: Optional[Dict[str, Any]] = None,
        severity: str = "error",
    ) -> InvariantViolation:
        violation = InvariantViolation(
            violation_id=f"{subject_type}-{subject_id}-{rule_name}-{len(self.violations) + 1}",
            subject_type=subject_type,
            subject_id=str(subject_id),
            rule_name=rule_name,
            context=context or {},
            created_at=datetime.now(timezone.utc),
            severity=severity,
        )
        self.violations.append(violation)
        return violation

    def validate_artifact(self, artifact, provenance_status=None) -> bool:
        if artifact is None:
            self._record_violation("artifact", "unknown", "artifact_required", {"reason": "artifact is missing"})
            return False

        artifact_id = getattr(artifact, "artifact_id", None)
        if artifact_id is None or str(artifact_id).strip() == "":
            self._record_violation("artifact", artifact_id or "unknown", "artifact_must_have_durable_id", {"artifact": artifact})
            return False

        if provenance_status is not None and hasattr(artifact, "provenance_status"):
            artifact.provenance_status = str(provenance_status)

        return True

    def validate_decision(self, decision) -> bool:
        if decision is None:
            self._record_violation("decision", "unknown", "decision_required", {"reason": "decision is missing"})
            return False

        decision_id = getattr(decision, "decision_id", None)
        if decision_id is None or str(decision_id).strip() == "":
            self._record_violation("decision", decision_id or "unknown", "decision_must_have_id", {"decision": decision})
            return False

        if getattr(decision, "state", None) == "SUPERSEDED" and getattr(decision, "current", True) is True:
            self._record_violation(
                "decision",
                decision_id,
                "superseded_decision_cannot_be_current",
                {"state": getattr(decision, "state", None), "current": getattr(decision, "current", True)},
            )
            return False

        approval = getattr(decision, "approval", None)
        if approval is not None and str(approval).strip() == "":
            self._record_violation("decision", decision_id, "decision_approval_required", {"decision": decision_id})
            return False

        return True

    def validate_approval(
        self,
        approval,
        provenance_record=None,
        decision_record=None,
        *,
        require_provenance: bool = True,
        require_decision_record: bool = True,
    ) -> bool:
        if approval is None:
            self._record_violation("approval", "unknown", "approval_required", {"reason": "approval record is missing"})
            return False

        reviewer = getattr(approval, "reviewer", None)
        if reviewer is None or str(reviewer).strip() == "":
            self._record_violation("approval", getattr(approval, "approval_id", "unknown"), "approval_must_be_attributable", {"reviewer": reviewer})
            return False

        decision_id = getattr(approval, "decision_id", None)
        if require_decision_record and decision_record is None:
            self._record_violation("approval", getattr(approval, "approval_id", "unknown"), "decision_must_be_recorded", {"approval": approval, "decision_id": decision_id})
            return False

        if provenance_record is not None and getattr(provenance_record, "status", None) == ProvenanceStatus.REJECTED:
            self._record_violation(
                "artifact",
                getattr(approval, "target_id", "unknown"),
                "rejected_artifact_cannot_be_approved",
                {"status": str(provenance_record.status), "target_id": getattr(approval, "target_id", "unknown")},
            )
            return False

        if require_provenance and provenance_record is None:
            self._record_violation(
                "artifact",
                getattr(approval, "target_id", "unknown"),
                "artifact_must_have_provenance_before_approval",
                {"target_id": getattr(approval, "target_id", "unknown")},
            )
            return False

        return True

    def validate_branch(self, branch) -> bool:
        if branch is None:
            self._record_violation("branch", "unknown", "branch_required", {"reason": "branch is missing"})
            return False

        branch_id = getattr(branch, "branch_id", None)
        if branch_id is None or str(branch_id).strip() == "":
            self._record_violation("branch", branch_id or "unknown", "branch_must_have_id", {"branch": branch})
            return False

        parent_id = getattr(branch, "parent_id", None)
        if parent_id is None or str(parent_id).strip() == "":
            self._record_violation("branch", branch_id, "branch_must_retain_parent_lineage", {"parent_id": parent_id, "branch_id": branch_id})
            return False

        return True

    def validate_lifecycle_transition(self, record, new_state) -> bool:
        if record is None:
            self._record_violation("lifecycle", "unknown", "record_required", {"reason": "lifecycle record is missing"})
            return False

        state = getattr(record, "state", "")
        if state is None or str(state).strip() == "":
            self._record_violation("lifecycle", getattr(record, "artifact_id", "unknown"), "lifecycle_state_required", {"record": record})
            return False

        valid_states = {
            "IDEA": ["VALIDATED"],
            "VALIDATED": ["DESIGNED"],
            "DESIGNED": ["IMPLEMENTED"],
            "IMPLEMENTED": ["TESTING"],
            "TESTING": ["DEPLOYED"],
            "DEPLOYED": ["ARCHIVED"],
        }

        if new_state not in valid_states.get(state, []):
            self._record_violation(
                "lifecycle",
                getattr(record, "artifact_id", "unknown"),
                "invalid_lifecycle_transition",
                {"from_state": state, "to_state": new_state},
            )
            return False

        return True


__all__ = ["InvariantEngine"]
