from typing import List, Optional

from innovation_os.branches.models import Branch
from innovation_os.invariants import InvariantEngine
from innovation_os.lineage import LineageEngine


class BranchEngine:

    def __init__(self, lineage_engine: Optional[LineageEngine] = None, invariant_engine: Optional[InvariantEngine] = None):
        self.branches: List[Branch] = []
        self.lineage_engine = lineage_engine or LineageEngine()
        self.invariant_engine = invariant_engine or InvariantEngine()

    def create_branch(
        self,
        branch_id: str,
        parent_id: str,
        problem_id: str,
        title: str,
        description: str,
        status: str = "ACTIVE",
    ) -> Branch:

        branch = Branch(
            branch_id=branch_id,
            parent_id=parent_id,
            problem_id=problem_id,
            title=title,
            description=description,
            status=status,
        )

        if self.get_branch(branch_id) is not None:
            raise ValueError(f"Branch already exists: {branch_id!r}")

        if not self.invariant_engine.validate_branch(branch):
            raise ValueError(f"Branch invariant violation for {branch_id!r}")

        lineage_record = self.lineage_engine.record_lineage_transition(
            branch.branch_id,
            {
                "branch_id": branch.branch_id,
                "parent_id": branch.parent_id,
                "problem_id": branch.problem_id,
                "title": branch.title,
                "description": branch.description,
                "status": branch.status,
            },
            parent_artifact_id=branch.parent_id,
            branch_id=branch.branch_id,
            provenance_status=status,
        )
        branch.lineage_hash = lineage_record.lineage_hash

        self.branches.append(branch)

        return branch

    def get_branch(
        self,
        branch_id: str,
    ) -> Optional[Branch]:

        for branch in self.branches:
            if branch.branch_id == branch_id:
                return branch

        return None

    def get_child_branches(
        self,
        parent_id: str,
    ) -> List[Branch]:

        return [
            branch
            for branch in self.branches
            if branch.parent_id == parent_id
        ]

    def update_status(
        self,
        branch_id: str,
        status: str,
    ) -> Optional[Branch]:

        branch = self.get_branch(branch_id)

        if branch:
            if status == branch.status:
                return branch
            if status not in {"ACTIVE", "REVIEW", "MERGED", "ARCHIVED"}:
                raise ValueError(f"Invalid branch status: {status!r}")
            branch.status = status
            lineage_record = self.lineage_engine.record_lineage_transition(
                branch.branch_id,
                {
                    "branch_id": branch.branch_id,
                    "parent_id": branch.parent_id,
                    "problem_id": branch.problem_id,
                    "title": branch.title,
                    "description": branch.description,
                    "status": branch.status,
                },
                parent_artifact_id=branch.parent_id,
                branch_id=branch.branch_id,
                provenance_status=status,
            )
            branch.lineage_hash = lineage_record.lineage_hash

        return branch
