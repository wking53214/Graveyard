from typing import List, Optional

from innovation_os.governance.models import (
    ApprovalRecord,
)
from innovation_os.invariants import InvariantEngine
from innovation_os.lineage import LineageEngine


class ApprovalEngine:

    def __init__(
        self,
        provenance_engine=None,
        decision_engine=None,
        lineage_engine: Optional[LineageEngine] = None,
        invariant_engine: Optional[InvariantEngine] = None,
    ):
        self.records: List[ApprovalRecord] = []
        self.provenance_engine = provenance_engine
        self.decision_engine = decision_engine
        self.lineage_engine = lineage_engine or LineageEngine()
        self.invariant_engine = invariant_engine or InvariantEngine()

    def submit_approval(
        self,
        approval_id: str,
        target_id: str,
        reviewer: str,
        decision: str,
        rationale: str,
        *,
        decision_id: Optional[str] = None,
        branch_id: Optional[str] = None,
    ) -> ApprovalRecord:

        record = ApprovalRecord(
            approval_id=approval_id,
            target_id=target_id,
            reviewer=reviewer,
            decision=decision,
            rationale=rationale,
            decision_id=decision_id,
        )

        provenance_record = None
        if self.provenance_engine is not None:
            provenance_record = self.provenance_engine.get(target_id)

        decision_record = None
        if self.decision_engine is not None:
            if decision_id is not None:
                decision_record = self.decision_engine.get_decision(decision_id)
            else:
                decision_record = next(
                    (
                        entry
                        for entry in self.decision_engine.decisions
                        if entry.decision_id == target_id or entry.problem_id == target_id
                    ),
                    None,
                )

        if not self.invariant_engine.validate_approval(
            record,
            provenance_record=provenance_record,
            decision_record=decision_record,
            require_provenance=self.provenance_engine is not None,
            require_decision_record=self.decision_engine is not None,
        ):
            raise ValueError(f"Approval invariant violation for {approval_id!r}")

        record.lineage_hash = self.lineage_engine.record_lineage_transition(
            approval_id,
            {
                "approval_id": approval_id,
                "target_id": target_id,
                "reviewer": reviewer,
                "decision": decision,
                "rationale": rationale,
                "decision_id": decision_id,
                "branch_id": branch_id,
            },
            branch_id=branch_id,
            provenance_status=getattr(provenance_record, "status", None),
        ).lineage_hash

        self.records.append(record)

        return record

    def get_approval(
        self,
        approval_id: str,
    ) -> Optional[ApprovalRecord]:

        for record in self.records:
            if record.approval_id == approval_id:
                return record

        return None

    def get_for_target(
        self,
        target_id: str,
    ) -> List[ApprovalRecord]:

        return [
            record
            for record in self.records
            if record.target_id == target_id
        ]
