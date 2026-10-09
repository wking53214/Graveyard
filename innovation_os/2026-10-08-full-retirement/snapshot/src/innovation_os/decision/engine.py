from typing import List, Optional

from innovation_os.decision.models import Decision
from innovation_os.invariants import InvariantEngine
from innovation_os.lineage import LineageEngine


class DecisionEngine:
    def __init__(self, lineage_engine: Optional[LineageEngine] = None, invariant_engine: Optional[InvariantEngine] = None):
        self.decisions: List[Decision] = []
        self.lineage_engine = lineage_engine or LineageEngine()
        self.invariant_engine = invariant_engine or InvariantEngine()

    def create_decision(
        self,
        decision_id: str,
        problem_id: str,
        context: str,
        options: List[str],
        selected_option: str,
        rejected_options: List[str],
        assumptions: List[str],
        confidence: float,
        approval: str,
        alternatives: List[str] = None,
        *,
        branch_id: Optional[str] = None,
    ) -> Decision:

        approval_value = str(approval or "")
        decision = Decision(
            decision_id=decision_id,
            problem_id=problem_id,
            context=context,
            options=options,
            selected_option=selected_option,
            rejected_options=rejected_options,
            assumptions=assumptions,
            confidence=confidence,
            approval=approval,
            alternatives=alternatives or [],
            state="SUPERSEDED" if approval_value.upper().startswith("SUPERSEDED") else "CURRENT",
            current=not approval_value.upper().startswith("SUPERSEDED"),
            branch_id=branch_id,
        )

        if not self.invariant_engine.validate_decision(decision):
            raise ValueError(f"Decision invariant violation for {decision_id!r}")

        lineage_record = self.lineage_engine.record_lineage_transition(
            decision.decision_id,
            {
                "decision_id": decision.decision_id,
                "problem_id": decision.problem_id,
                "context": decision.context,
                "selected_option": decision.selected_option,
                "approval": decision.approval,
                "state": decision.state,
                "branch_id": decision.branch_id,
            },
            branch_id=decision.branch_id,
            provenance_status=decision.state,
        )
        decision.lineage_hash = lineage_record.lineage_hash

        self.decisions.append(decision)

        return decision

    def get_decision(
        self,
        decision_id: str,
    ) -> Optional[Decision]:

        for decision in self.decisions:
            if decision.decision_id == decision_id:
                return decision

        return None

    def get_decisions_for_problem(
        self,
        problem_id: str,
    ) -> List[Decision]:

        return [
            decision
            for decision in self.decisions
            if decision.problem_id == problem_id
        ]
