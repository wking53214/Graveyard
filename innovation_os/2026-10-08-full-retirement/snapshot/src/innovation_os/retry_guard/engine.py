import hashlib
import json
from typing import Optional

from .models import RetryAttempt


class RetryGuardEngine:

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.attempts = []

    @staticmethod
    def build_fingerprint(
        artifact_hash: str,
        branch_id: str,
        parent_artifact_id: Optional[str],
        decision_state: str,
        evidence_version: str,
        retry_count: int = 0,
    ) -> str:
        payload = {
            "artifact_hash": artifact_hash,
            "branch_id": branch_id,
            "parent_artifact_id": parent_artifact_id or "",
            "decision_state": decision_state,
            "evidence_version": evidence_version,
            "retry_count": retry_count,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def register_attempt(
        self,
        attempt_id: str,
        artifact_id: str,
        branch_id: str,
        parent_artifact_id: Optional[str],
        evidence_id: str,
        decision_state: str,
        artifact_hash: str,
        evidence_version: str,
        retry_count: int = 0,
    ) -> RetryAttempt:
        fingerprint = self.build_fingerprint(
            artifact_hash,
            branch_id,
            parent_artifact_id,
            decision_state,
            evidence_version,
            retry_count,
        )
        attempt = RetryAttempt(
            attempt_id=attempt_id,
            artifact_id=artifact_id,
            branch_id=branch_id,
            parent_artifact_id=parent_artifact_id,
            evidence_id=evidence_id,
            decision_state=decision_state,
            fingerprint=fingerprint,
            retry_count=retry_count,
            artifact_hash=artifact_hash,
            evidence_version=evidence_version,
        )
        self.attempts.append(attempt)
        return attempt

    def detect_cycle(
        self,
        artifact_id: str,
        branch_id: str,
        parent_artifact_id: Optional[str],
        evidence_id: str,
        evidence_version: str,
        artifact_hash: str,
    ) -> bool:
        matching_indexes = [
            index
            for index, attempt in enumerate(self.attempts)
            if attempt.artifact_hash == artifact_hash
            and attempt.artifact_id == artifact_id
            and attempt.branch_id == branch_id
            and attempt.parent_artifact_id == parent_artifact_id
            and attempt.evidence_id == evidence_id
            and attempt.evidence_version == evidence_version
        ]
        return any(
            right - left > 1
            for left, right in zip(matching_indexes, matching_indexes[1:])
        )

    def assess_repetition(
        self,
        artifact_id: str,
        branch_id: str,
        parent_artifact_id: Optional[str],
        evidence_id: str,
        decision_state: str,
        artifact_hash: str,
        evidence_version: str,
    ) -> bool:
        fingerprint = self.build_fingerprint(
            artifact_hash,
            branch_id,
            parent_artifact_id,
            decision_state,
            evidence_version,
        )
        prior = [
            attempt
            for attempt in self.attempts
            if attempt.artifact_id == artifact_id and attempt.fingerprint == fingerprint
        ]
        if not prior:
            return False

        recent = prior[-1]
        return (
            recent.evidence_id == evidence_id
            and recent.branch_id == branch_id
            and recent.parent_artifact_id == parent_artifact_id
            and recent.decision_state == decision_state
        )

    def allow_reentry(
        self,
        artifact_id: str,
        branch_id: str,
        parent_artifact_id: Optional[str],
        evidence_id: str,
        decision_state: str,
        artifact_hash: str,
        evidence_version: str,
    ) -> bool:
        if self.assess_repetition(
            artifact_id,
            branch_id,
            parent_artifact_id,
            evidence_id,
            decision_state,
            artifact_hash,
            evidence_version,
        ):
            same = [
                attempt
                for attempt in self.attempts
                if attempt.artifact_id == artifact_id
                and attempt.branch_id == branch_id
                and attempt.parent_artifact_id == parent_artifact_id
                and attempt.decision_state == decision_state
                and attempt.evidence_id == evidence_id
            ]
            return len(same) < self.max_retries

        return True

    def flag_oscillation(
        self,
        artifact_id: str,
        branch_id: str,
        parent_artifact_id: Optional[str],
        evidence_id: str,
        decision_state: str,
        artifact_hash: str,
        evidence_version: str,
    ) -> bool:
        same = [
            attempt
            for attempt in self.attempts
            if attempt.artifact_id == artifact_id
            and attempt.branch_id == branch_id
            and attempt.parent_artifact_id == parent_artifact_id
            and attempt.decision_state == decision_state
            and attempt.evidence_id == evidence_id
        ]
        return len(same) >= self.max_retries


__all__ = ["RetryGuardEngine"]
