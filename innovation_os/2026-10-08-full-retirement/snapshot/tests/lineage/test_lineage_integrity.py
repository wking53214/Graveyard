from innovation_os.lineage import LineageEngine
from innovation_os.registry.artifact_registry import Artifact, ArtifactRegistry
from innovation_os.provenance import ProvenanceEngine, ProvenanceStatus
from innovation_os.branches.engine import BranchEngine


def test_changed_artifact_after_creation_is_detectably_different():
    payload_a = {"artifact_id": "ART-100", "name": "draft", "status": "draft"}
    payload_b = {"artifact_id": "ART-100", "name": "draft", "status": "final"}

    hash_a = LineageEngine.hash_artifact(LineageEngine.canonicalize_artifact(payload_a))
    hash_b = LineageEngine.hash_artifact(LineageEngine.canonicalize_artifact(payload_b))

    assert hash_a != hash_b


def test_lineage_hash_is_preserved_across_registration():
    provenance = ProvenanceEngine()
    lineage = LineageEngine()
    registry = ArtifactRegistry(provenance_engine=provenance, lineage_engine=lineage)

    artifact = Artifact(
        artifact_id="ART-101",
        artifact_type="CODE",
        name="module.py",
        source="/tmp/module.py",
        project_id="project-1",
        metadata={"language": "python"},
    )

    registered = registry.register(artifact, provenance_status=ProvenanceStatus.USER_ESTABLISHED)

    assert registered.canonical_hash
    assert registered.lineage_hash
    assert lineage.verify_lineage("ART-101")


def test_branch_ancestry_is_retained():
    branch = BranchEngine().create_branch(
        branch_id="BRANCH-200",
        parent_id="ROOT-1",
        problem_id="PROBLEM-200",
        title="ancestry",
        description="parent retained",
    )

    assert branch.parent_id == "ROOT-1"
    assert branch.lineage_hash


def test_parent_artifact_link_is_preserved():
    lineage = LineageEngine()
    lineage.record_lineage_transition("PARENT-1", {"artifact_id": "PARENT-1", "kind": "source"})
    lineage.link_parent_artifact("CHILD-1", "PARENT-1")

    assert lineage.records["CHILD-1"].parent_artifact_id == "PARENT-1"
    assert lineage.records["CHILD-1"].parent_hash


def test_export_persistence_boundary_verifies_lineage():
    lineage = LineageEngine()
    record = lineage.record_lineage_transition(
        "EXPORT-1",
        {"artifact_id": "EXPORT-1", "content": "persisted"},
    )

    assert record.lineage_hash
    assert lineage.verify_lineage("EXPORT-1")


def test_lineage_verification_detects_record_mutation():
    lineage = LineageEngine()
    lineage.record_lineage_transition(
        "MUTATION-1",
        {"artifact_id": "MUTATION-1", "content": "original"},
    )

    lineage.records["MUTATION-1"].canonical_hash = "tampered"

    assert not lineage.verify_lineage("MUTATION-1")


def test_child_lineage_verification_checks_parent_hash():
    lineage = LineageEngine()
    lineage.record_lineage_transition(
        "PARENT-2",
        {"artifact_id": "PARENT-2", "content": "source"},
    )
    lineage.record_lineage_transition(
        "CHILD-2",
        {"artifact_id": "CHILD-2", "content": "derived"},
        parent_artifact_id="PARENT-2",
    )

    lineage.records["PARENT-2"].canonical_hash = "tampered"

    assert not lineage.verify_lineage("CHILD-2")


def test_lineage_events_are_chained_and_verifiable():
    lineage = LineageEngine()
    lineage.record_lineage_transition("EVENT-1", {"value": 1})
    lineage.record_lineage_transition("EVENT-1", {"value": 2}, version=2)

    assert lineage.verify_events()
    assert lineage.snapshot("EVENT-1") == b'{"value":2}'

    lineage.events[1].payload["canonical_hash"] = "tampered"

    assert not lineage.verify_events()


def test_artifact_registry_detects_mutation_against_snapshot():
    registry = ArtifactRegistry(lineage_engine=LineageEngine())
    artifact = registry.register(
        Artifact(
            artifact_id="ART-102",
            artifact_type="CODE",
            name="module.py",
            source="/tmp/module.py",
            project_id="project-1",
            metadata={"language": "python"},
        )
    )

    assert registry.verify(artifact.artifact_id)
    artifact.metadata["language"] = "ruby"

    assert not registry.verify(artifact.artifact_id)


def test_lineage_events_and_snapshots_survive_restart(tmp_path):
    database = tmp_path / "lineage.sqlite"
    first = LineageEngine(storage_path=str(database))
    first.record_lineage_transition(
        "PERSISTED-1",
        {"artifact_id": "PERSISTED-1", "content": "durable"},
    )

    second = LineageEngine(storage_path=str(database))

    assert second.snapshot("PERSISTED-1") == first.snapshot("PERSISTED-1")
    assert second.verify_events()
    assert second.verify_lineage("PERSISTED-1")
