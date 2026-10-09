"""
EDDP INGESTION AUTHENTICATION

Provides keyed (HMAC-SHA256) authentication for payloads entering the EDDP
pipeline.

This is distinct from the integrity hashing already performed downstream by
AggregatedMetricScorer. That hash is an unkeyed SHA-256 checksum: it detects
accidental alteration, but anyone can recompute it, so it proves nothing about
origin. The HMAC here is computed with a shared secret, so a valid signature
demonstrates the payload was produced by a holder of that secret.

Origin: SecureDataIngestionPipeline, relocated from CODE
(content-pipeline-eddp-classes.py). Two defects in the original were corrected
during relocation; both are documented inline below.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from collections import deque
from typing import Any, Dict, Optional

MODULE_REGISTRY: Dict[str, type] = {}


def register_as_module(cls: type) -> type:
    """Governance handshake validation decorator.

    Matches the convention used by metric_assessment_telemetry_dispatch_adapter
    so modules from both files can be sequenced by the same orchestrator.
    """
    MODULE_REGISTRY[cls.__name__] = cls
    setattr(cls, "_is_authenticated_module", True)
    return cls


class SignatureVerificationError(Exception):
    """Raised when an inbound payload carries a signature that does not verify."""


class SecureDataIngestionPipeline:
    """Schema-validates, signs, and verifies inbound payloads.

    DEFECT 1 CORRECTED: the original referenced `deque` without importing it,
    so constructing this class raised NameError immediately. `collections.deque`
    is now imported.

    DEFECT 2 CORRECTED: the original computed a signature and then verified that
    same freshly-computed signature against itself, which is true by
    construction and authenticates nothing. Verification now runs against a
    signature supplied on the inbound payload, which is the only form of the
    check that carries meaning. Payloads arriving unsigned are signed on
    ingest and marked as such.
    """

    SIGNATURE_FIELD = "cryptographic_signature"
    ORIGIN_FIELD = "signature_origin"

    # Fields the pipeline stamps ONTO a payload as a record of what it decided.
    # They are annotations about the authentication, not part of the authenticated
    # content, so neither signing nor verification covers them.
    #
    # DEFECT 3 CORRECTED: only SIGNATURE_FIELD was excluded. ORIGIN_FIELD is
    # written after the signature is computed, so the moment a payload signed at
    # ingest came back through -- a retry, a replay, a second stage -- verification
    # ran over bytes that now included a field the signature could not have
    # covered, and the pipeline rejected its own output as forged.
    UNSIGNED_FIELDS = frozenset({SIGNATURE_FIELD, ORIGIN_FIELD})

    def __init__(self, cryptographic_secret: str, max_log_capacity: int = 1000):
        self.cryptographic_secret: bytes = cryptographic_secret.encode()
        self.bounded_audit_history: deque = deque(maxlen=max_log_capacity)

    @staticmethod
    def normalize_payload_spacing(payload: Dict[str, Any]) -> Dict[str, Any]:
        copied_payload = dict(payload)
        body = copied_payload.get("body_content")
        if isinstance(body, str):
            copied_payload["body_content"] = " ".join(body.split())
        return copied_payload

    @staticmethod
    def validate_schema_constraints(payload: Dict[str, Any]) -> bool:
        body = payload.get("body_content")
        if not isinstance(body, str):
            return False
        if len(body) == 0 or len(body) > 5000:
            return False
        if not isinstance(payload.get("metadata_context"), dict):
            return False
        return True

    def generate_payload_signature(self, payload: Dict[str, Any]) -> str:
        """Deterministic HMAC-SHA256 over the payload, excluding the fields the
        pipeline stamps on afterwards so signing and verification cover
        identical bytes on every pass, not only the first."""
        signable = {
            k: v for k, v in payload.items() if k not in self.UNSIGNED_FIELDS
        }
        canonical_bytes = json.dumps(
            signable,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode()
        return hmac.new(
            self.cryptographic_secret,
            canonical_bytes,
            hashlib.sha256,
        ).hexdigest()

    def verify_signature_integrity(
        self, payload: Dict[str, Any], inbound_signature: str
    ) -> bool:
        expected_signature = self.generate_payload_signature(payload)
        return hmac.compare_digest(expected_signature, inbound_signature)

    def record_pipeline_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        self.bounded_audit_history.append(
            {
                "timestamp": time.time(),
                "event_classification": event_type,
                "associated_payload": payload,
            }
        )

    def execute_ingestion_audit(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        normalized_payload = self.normalize_payload_spacing(raw_payload)

        if not self.validate_schema_constraints(normalized_payload):
            self.record_pipeline_event(
                "TRANSACTION_REJECTED_INVALID_SCHEMA", normalized_payload
            )
            raise ValueError(
                "Inbound data payload failed structural schema requirements."
            )

        inbound_signature: Optional[str] = normalized_payload.get(self.SIGNATURE_FIELD)

        if inbound_signature is not None:
            if not self.verify_signature_integrity(
                normalized_payload, inbound_signature
            ):
                self.record_pipeline_event(
                    "TRANSACTION_REJECTED_SIGNATURE_MISMATCH", normalized_payload
                )
                raise SignatureVerificationError(
                    "Inbound signature failed HMAC verification against the "
                    "configured secret. Payload origin is unauthenticated."
                )
            normalized_payload[self.ORIGIN_FIELD] = "verified_inbound"
            self.record_pipeline_event(
                "TRANSACTION_ACCEPTED_SIGNATURE_VERIFIED", normalized_payload
            )
            return normalized_payload

        signed_output_payload = dict(normalized_payload)
        signed_output_payload[self.SIGNATURE_FIELD] = self.generate_payload_signature(
            signed_output_payload
        )
        signed_output_payload[self.ORIGIN_FIELD] = "signed_at_ingest"
        self.record_pipeline_event(
            "TRANSACTION_ACCEPTED_SIGNED_AT_INGEST", signed_output_payload
        )
        return signed_output_payload


@register_as_module
class IngestionAuthenticationModule:
    """Pipeline-module wrapper exposing the standard .process() interface.

    Reads its secret from EDDP_SIGNING_SECRET. With no secret configured it
    falls back to a random secret generated for this instance. That secret is
    never published, so nothing signed elsewhere verifies against it: inbound
    signatures are rejected and only locally signed envelopes pass. The
    fallback is reported as ``placeholder_secret_in_use`` so a deployment can
    see that it has no shared secret.
    """

    def __init__(
        self,
        cryptographic_secret: Optional[str] = None,
        require_envelope: bool = True,
    ):
        # Fail closed: a payload with no ingestion envelope has not been
        # authenticated, so by default it is halted rather than passed on.
        # require_envelope=False restores report-and-continue for callers
        # that deliberately handle unauthenticated payloads themselves.
        self.require_envelope = require_envelope
        secret = cryptographic_secret or os.getenv("EDDP_SIGNING_SECRET")
        self.using_placeholder_secret = not secret
        if not secret:
            secret = secrets.token_hex(32)
        self.pipeline = SecureDataIngestionPipeline(secret)

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if payload.get("halted"):
            return payload

        headers = payload.setdefault(
            "_gaps_headers",
            {"metadata": {}, "risk_metrics": {}, "structural_indices": {}},
        )

        envelope = payload.get("ingestion_envelope")
        if envelope is None:
            if self.require_envelope:
                payload["halted"] = True
                payload["block_reason"] = "no ingestion envelope: payload is unauthenticated"
                headers["metadata"]["ingestion_authentication"] = "rejected_no_envelope"
                headers["risk_metrics"]["ingestion_authenticated"] = False
                return payload
            headers["metadata"]["ingestion_authentication"] = "skipped_no_envelope"
            return payload

        try:
            authenticated = self.pipeline.execute_ingestion_audit(envelope)
        except (ValueError, SignatureVerificationError) as rejection:
            payload["halted"] = True
            payload["block_reason"] = str(rejection)
            headers["risk_metrics"]["ingestion_authenticated"] = False
            return payload

        payload["ingestion_envelope"] = authenticated
        headers["risk_metrics"]["ingestion_authenticated"] = True
        headers["metadata"]["signature_origin"] = authenticated.get("signature_origin")
        headers["metadata"]["placeholder_secret_in_use"] = self.using_placeholder_secret
        return payload
