import pytest

from innovation_os.branches.engine import BranchEngine
from innovation_os.governance.engine import ApprovalEngine
from innovation_os.lifecycle.state_machine import InnovationLifecycleEngine
from innovation_os.provenance import ProvenanceEngine, ProvenanceStatus


def test_artifact_without_provenance_cannot_be_approved():
    engine = ApprovalEngine(provenance_engine=ProvenanceEngine())

    with pytest.raises(ValueError):
        engine.submit_approval(
            approval_id="APPROVAL-001",
            target_id="ART-001",
            reviewer="Alice",
            decision="APPROVED",
            rationale="Ready",
        )


def test_rejected_artifact_cannot_silently_become_approved():
    provenance = ProvenanceEngine()
    provenance.register("ART-002", ProvenanceStatus.REJECTED, source="manual")
    engine = ApprovalEngine(provenance_engine=provenance)

    with pytest.raises(ValueError):
        engine.submit_approval(
            approval_id="APPROVAL-002",
            target_id="ART-002",
            reviewer="Alice",
            decision="APPROVED",
            rationale="Override failed",
        )


def test_decision_without_authority_fails_validation():
    engine = ApprovalEngine()

    with pytest.raises(ValueError):
        engine.submit_approval(
            approval_id="APPROVAL-003",
            target_id="ART-003",
            reviewer="   ",
            decision="APPROVED",
            rationale="Needs reviewer",
        )


def test_branch_without_parent_lineage_fails_validation():
    engine = BranchEngine()

    with pytest.raises(ValueError):
        engine.create_branch(
            branch_id="BRANCH-001",
            parent_id="",
            problem_id="PROBLEM-001",
            title="Broken branch",
            description="Missing parent",
        )


def test_invalid_lifecycle_transition_is_rejected():
    engine = InnovationLifecycleEngine()
    engine.create("ART-004")

    assert not engine.transition("ART-004", "DEPLOYED")
