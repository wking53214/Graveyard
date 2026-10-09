from innovation_os.branches.engine import (
    BranchEngine,
)


def test_create_branch():

    engine = BranchEngine()

    branch = engine.create_branch(
        branch_id="BRANCH-0001",
        parent_id="CEE-0001",
        problem_id="PROBLEM-0001",
        title="Healthcare efficiency path",
        description="Explore workflow improvements",
    )

    assert branch.branch_id == "BRANCH-0001"
    assert branch.status == "ACTIVE"


def test_get_branch():

    engine = BranchEngine()

    engine.create_branch(
        branch_id="BRANCH-0002",
        parent_id="CEE-0001",
        problem_id="PROBLEM-0002",
        title="Automation path",
        description="Explore automation options",
    )

    branch = engine.get_branch(
        "BRANCH-0002"
    )

    assert branch is not None
    assert branch.problem_id == "PROBLEM-0002"


def test_child_branches():

    engine = BranchEngine()

    engine.create_branch(
        branch_id="BRANCH-0001",
        parent_id="ROOT",
        problem_id="PROBLEM-0001",
        title="Parent branch",
        description="Root exploration",
    )

    engine.create_branch(
        branch_id="BRANCH-0002",
        parent_id="ROOT",
        problem_id="PROBLEM-0001",
        title="Child branch",
        description="Alternative exploration",
    )

    children = engine.get_child_branches(
        "ROOT"
    )

    assert len(children) == 2


def test_update_branch_status():

    engine = BranchEngine()

    engine.create_branch(
        branch_id="BRANCH-0003",
        parent_id="ROOT",
        problem_id="PROBLEM-0003",
        title="Review branch",
        description="Needs review",
    )

    branch = engine.update_status(
        "BRANCH-0003",
        "REVIEW",
    )

    assert branch.status == "REVIEW"


def test_branch_status_update_refreshes_lineage():
    engine = BranchEngine()
    branch = engine.create_branch(
        branch_id="BRANCH-0004",
        parent_id="ROOT-0004",
        problem_id="PROBLEM-0004",
        title="Status lineage",
        description="status changes are recorded",
    )
    original_hash = branch.lineage_hash

    engine.update_status("BRANCH-0004", "REVIEW")

    assert branch.lineage_hash != original_hash
    assert engine.lineage_engine.verify_events()


def test_duplicate_branch_id_is_rejected():
    engine = BranchEngine()
    kwargs = {
        "branch_id": "BRANCH-0005",
        "parent_id": "ROOT-0005",
        "problem_id": "PROBLEM-0005",
        "title": "Duplicate",
        "description": "duplicate IDs are unsafe",
    }
    engine.create_branch(**kwargs)

    try:
        engine.create_branch(**kwargs)
    except ValueError as error:
        assert "already exists" in str(error)
    else:
        raise AssertionError("Expected duplicate branch ID to be rejected")
