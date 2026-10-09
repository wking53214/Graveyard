from dataclasses import dataclass
import uuid
from innovation_os.intelligence.contracts import IntelligenceArtifact
from innovation_os.lineage import LineageEngine
from innovation_os.retry_guard import RetryGuardEngine


@dataclass
class IntelligenceRuntime:

    pipeline: object

    memory: object

    retry_guard: object = None

    @staticmethod
    def _context_metadata(context):
        if isinstance(context, dict):
            return context
        return getattr(context, "metadata", {}) or {}

    def _guard_execution(self, input_data, context):
        if self.retry_guard is None:
            return

        metadata = self._context_metadata(context)
        artifact_hash = LineageEngine.hash_artifact(
            LineageEngine.canonicalize_artifact(input_data)
        )
        artifact_id = metadata.get("artifact_id", artifact_hash)
        branch_id = metadata.get("branch_id", "default")
        parent_artifact_id = metadata.get("parent_artifact_id")
        evidence_id = metadata.get("evidence_id", "")
        decision_state = metadata.get("decision_state", "UNSET")
        evidence_version = metadata.get("evidence_version", "unknown")

        if self.retry_guard.detect_cycle(
            artifact_id,
            branch_id,
            parent_artifact_id,
            evidence_id,
            evidence_version,
            artifact_hash,
        ):
            raise RuntimeError(
                f"Oscillation detected for artifact {artifact_id!r}"
            )

        if not self.retry_guard.allow_reentry(
            artifact_id,
            branch_id,
            parent_artifact_id,
            evidence_id,
            decision_state,
            artifact_hash,
            evidence_version,
        ):
            raise RuntimeError(
                f"Retry budget exhausted for artifact {artifact_id!r}"
            )

        self.retry_guard.register_attempt(
            attempt_id=str(uuid.uuid4()),
            artifact_id=artifact_id,
            branch_id=branch_id,
            parent_artifact_id=parent_artifact_id,
            evidence_id=evidence_id,
            decision_state=decision_state,
            artifact_hash=artifact_hash,
            evidence_version=evidence_version,
            retry_count=len(
                [
                    attempt
                    for attempt in self.retry_guard.attempts
                    if attempt.artifact_id == artifact_id
                    and attempt.branch_id == branch_id
                    and attempt.parent_artifact_id == parent_artifact_id
                    and attempt.evidence_id == evidence_id
                    and attempt.decision_state == decision_state
                    and attempt.fingerprint
                    == self.retry_guard.build_fingerprint(
                        artifact_hash,
                        branch_id,
                        parent_artifact_id,
                        decision_state,
                        evidence_version,
                    )
                ]
            ),
        )


    def _normalize(
        self,
        result
    ):

        if hasattr(
            result,
            "artifact_id"
        ):

            return result


        return IntelligenceArtifact(
            intelligence_type="runtime_result",
            source_system="intelligence_runtime",
            confidence=1.0,
            metadata={
                "payload": result
            },
        )



    def execute(
        self,
        input_data,
        context
    ):

        self._guard_execution(input_data, context)

        result = self.pipeline.process(
            input_data,
            context
        )


        artifact = self._normalize(
            result
        )


        self.memory.remember(
            artifact
        )


        return result
