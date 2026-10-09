"""Keyed (HMAC-SHA256) authentication for inbound payloads.

The original defect this module was relocated to correct was a verification
that checked a freshly-computed signature against itself, which is true by
construction. Several tests here exist specifically so that defect cannot come
back: they verify against a signature the checker did not compute, and they
assert that a wrong secret and a tampered body are both rejected.
"""

import json

import pytest

from eddp_ingestion_authentication import (
    IngestionAuthenticationModule,
    SecureDataIngestionPipeline,
    SignatureVerificationError,
)

SECRET = "test-secret"


def valid_envelope(**overrides):
    envelope = {
        "body_content": "Quarterly operational summary for distribution.",
        "metadata_context": {"source": "reporting-service"},
    }
    envelope.update(overrides)
    return envelope


class TestSchemaConstraints:
    def test_a_well_formed_envelope_validates(self):
        assert SecureDataIngestionPipeline.validate_schema_constraints(
            valid_envelope()
        )

    @pytest.mark.parametrize(
        "envelope",
        [
            {"metadata_context": {}},
            {"body_content": 42, "metadata_context": {}},
            {"body_content": None, "metadata_context": {}},
            {"body_content": "", "metadata_context": {}},
            {"body_content": "x" * 5001, "metadata_context": {}},
            {"body_content": "ok"},
            {"body_content": "ok", "metadata_context": "not-a-dict"},
        ],
    )
    def test_malformed_envelopes_are_rejected(self, envelope):
        assert not SecureDataIngestionPipeline.validate_schema_constraints(envelope)

    def test_the_boundary_length_is_admitted(self):
        assert SecureDataIngestionPipeline.validate_schema_constraints(
            {"body_content": "x" * 5000, "metadata_context": {}}
        )

    def test_schema_failure_raises_rather_than_passing_silently(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        with pytest.raises(ValueError):
            pipeline.execute_ingestion_audit({"body_content": ""})

    def test_a_rejection_is_recorded_in_the_audit_history(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        with pytest.raises(ValueError):
            pipeline.execute_ingestion_audit({"body_content": ""})
        assert [e["event_classification"] for e in pipeline.bounded_audit_history] == [
            "TRANSACTION_REJECTED_INVALID_SCHEMA"
        ]


class TestNormalization:
    def test_runs_of_whitespace_collapse(self):
        out = SecureDataIngestionPipeline.normalize_payload_spacing(
            {"body_content": "a   b\n\tc  "}
        )
        assert out["body_content"] == "a b c"

    def test_a_non_string_body_is_left_alone_for_the_schema_check_to_reject(self):
        out = SecureDataIngestionPipeline.normalize_payload_spacing(
            {"body_content": 42}
        )
        assert out["body_content"] == 42

    def test_normalization_does_not_mutate_the_caller_s_dict(self):
        original = {"body_content": "a   b"}
        SecureDataIngestionPipeline.normalize_payload_spacing(original)
        assert original["body_content"] == "a   b"

    def test_signing_is_stable_across_equivalent_spacing(self):
        """Normalization happens before signing, so two envelopes that differ
        only in whitespace must produce the same signature."""
        pipeline = SecureDataIngestionPipeline(SECRET)
        spaced = pipeline.execute_ingestion_audit(
            valid_envelope(body_content="one   two")
        )
        tight = pipeline.execute_ingestion_audit(
            valid_envelope(body_content="one two")
        )
        assert spaced["cryptographic_signature"] == tight["cryptographic_signature"]


class TestSignatureGeneration:
    def test_signature_is_deterministic(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        envelope = valid_envelope()
        assert pipeline.generate_payload_signature(
            envelope
        ) == pipeline.generate_payload_signature(dict(envelope))

    def test_signature_is_independent_of_key_order(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        one = {"body_content": "x", "metadata_context": {"a": 1}}
        other = {"metadata_context": {"a": 1}, "body_content": "x"}
        assert pipeline.generate_payload_signature(
            one
        ) == pipeline.generate_payload_signature(other)

    def test_signature_excludes_the_signature_field_itself(self):
        """Signing and verification must cover identical bytes; if the field
        were included, no signature could ever verify."""
        pipeline = SecureDataIngestionPipeline(SECRET)
        bare = valid_envelope()
        carrying = valid_envelope(cryptographic_signature="whatever")
        assert pipeline.generate_payload_signature(
            bare
        ) == pipeline.generate_payload_signature(carrying)

    def test_a_different_secret_produces_a_different_signature(self):
        envelope = valid_envelope()
        mine = SecureDataIngestionPipeline(SECRET).generate_payload_signature(envelope)
        theirs = SecureDataIngestionPipeline("other").generate_payload_signature(
            envelope
        )
        assert mine != theirs

    def test_a_changed_body_produces_a_different_signature(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        assert pipeline.generate_payload_signature(
            valid_envelope()
        ) != pipeline.generate_payload_signature(valid_envelope(body_content="edited"))

    def test_the_signature_is_a_sha256_hex_digest(self):
        signature = SecureDataIngestionPipeline(SECRET).generate_payload_signature(
            valid_envelope()
        )
        assert len(signature) == 64
        int(signature, 16)


class TestVerification:
    def test_a_signature_this_checker_did_not_compute_verifies(self):
        """The signature is produced by an independent instance holding the
        same secret. This is the shape the original defect could not satisfy."""
        signer = SecureDataIngestionPipeline(SECRET)
        verifier = SecureDataIngestionPipeline(SECRET)
        envelope = valid_envelope()
        signature = signer.generate_payload_signature(envelope)

        assert verifier.verify_signature_integrity(envelope, signature) is True

    def test_a_forged_signature_is_refused(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        assert pipeline.verify_signature_integrity(valid_envelope(), "0" * 64) is False

    def test_a_signature_from_a_different_secret_is_refused(self):
        envelope = valid_envelope()
        foreign = SecureDataIngestionPipeline("other").generate_payload_signature(
            envelope
        )
        assert (
            SecureDataIngestionPipeline(SECRET).verify_signature_integrity(
                envelope, foreign
            )
            is False
        )

    def test_a_tampered_body_is_refused(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        signature = pipeline.generate_payload_signature(valid_envelope())
        tampered = valid_envelope(body_content="tampered")
        assert pipeline.verify_signature_integrity(tampered, signature) is False


class TestIngestionAudit:
    def test_an_unsigned_envelope_is_signed_at_ingest(self):
        out = SecureDataIngestionPipeline(SECRET).execute_ingestion_audit(
            valid_envelope()
        )
        assert out["signature_origin"] == "signed_at_ingest"
        assert len(out["cryptographic_signature"]) == 64

    def test_a_correctly_signed_envelope_is_accepted_as_verified(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        envelope = valid_envelope()
        envelope["cryptographic_signature"] = pipeline.generate_payload_signature(
            envelope
        )

        out = pipeline.execute_ingestion_audit(envelope)
        assert out["signature_origin"] == "verified_inbound"

    def test_a_forged_signature_halts_ingestion(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        with pytest.raises(SignatureVerificationError):
            pipeline.execute_ingestion_audit(
                valid_envelope(cryptographic_signature="0" * 64)
            )

    def test_every_outcome_is_recorded_with_its_own_classification(self):
        pipeline = SecureDataIngestionPipeline(SECRET)
        pipeline.execute_ingestion_audit(valid_envelope())
        with pytest.raises(SignatureVerificationError):
            pipeline.execute_ingestion_audit(
                valid_envelope(cryptographic_signature="0" * 64)
            )

        assert [e["event_classification"] for e in pipeline.bounded_audit_history] == [
            "TRANSACTION_ACCEPTED_SIGNED_AT_INGEST",
            "TRANSACTION_REJECTED_SIGNATURE_MISMATCH",
        ]

    def test_audit_history_is_bounded(self):
        """An unbounded audit log is a memory leak in a long-running ingest."""
        pipeline = SecureDataIngestionPipeline(SECRET, max_log_capacity=3)
        for index in range(10):
            pipeline.execute_ingestion_audit(
                valid_envelope(body_content=f"body {index}")
            )
        assert len(pipeline.bounded_audit_history) == 3

    def test_a_signed_envelope_verifies_on_a_second_pass(self):
        """A payload this pipeline signed must authenticate when it comes back.

        Ingest signs, then stamps signature_origin onto the payload. If that
        stamp is covered by the signature, the pipeline rejects its own output
        as forged the moment the envelope is re-presented -- which is what a
        replay, a retry, or a second stage in the chain does.
        """
        pipeline = SecureDataIngestionPipeline(SECRET)
        signed = pipeline.execute_ingestion_audit(valid_envelope())

        reverified = pipeline.execute_ingestion_audit(dict(signed))
        assert reverified["signature_origin"] == "verified_inbound"


class TestIngestionAuthenticationModule:
    def test_an_explicit_secret_wins_over_the_environment(self, monkeypatch):
        monkeypatch.setenv("EDDP_SIGNING_SECRET", "from-env")
        module = IngestionAuthenticationModule("explicit")
        assert module.using_placeholder_secret is False
        assert module.pipeline.cryptographic_secret == b"explicit"

    def test_the_environment_wins_over_the_placeholder(self, monkeypatch):
        monkeypatch.setenv("EDDP_SIGNING_SECRET", "from-env")
        module = IngestionAuthenticationModule()
        assert module.using_placeholder_secret is False
        assert module.pipeline.cryptographic_secret == b"from-env"

    def test_the_placeholder_is_the_last_resort_and_declares_itself(
        self, monkeypatch
    ):
        """A deployment running on the in-source secret has no authentication
        at all. The only acceptable behaviour is to say so."""
        monkeypatch.delenv("EDDP_SIGNING_SECRET", raising=False)
        module = IngestionAuthenticationModule()
        assert module.using_placeholder_secret is True

    def test_the_placeholder_status_reaches_the_headers(self, monkeypatch):
        monkeypatch.delenv("EDDP_SIGNING_SECRET", raising=False)
        out = IngestionAuthenticationModule().process(
            {"ingestion_envelope": valid_envelope()}
        )
        assert out["_gaps_headers"]["metadata"]["placeholder_secret_in_use"] is True

    def test_a_missing_envelope_halts_by_default(self):
        out = IngestionAuthenticationModule(SECRET).process({})
        headers = out["_gaps_headers"]
        assert out["halted"] is True
        assert "no ingestion envelope" in out["block_reason"]
        assert headers["metadata"]["ingestion_authentication"] == "rejected_no_envelope"
        assert headers["risk_metrics"]["ingestion_authenticated"] is False

    def test_a_missing_envelope_is_reported_when_explicitly_allowed(self):
        out = IngestionAuthenticationModule(SECRET, require_envelope=False).process({})
        headers = out["_gaps_headers"]
        assert not out.get("halted")
        assert headers["metadata"]["ingestion_authentication"] == "skipped_no_envelope"
        assert "ingestion_authenticated" not in headers["risk_metrics"]

    def test_a_valid_envelope_marks_the_payload_authenticated(self):
        out = IngestionAuthenticationModule(SECRET).process(
            {"ingestion_envelope": valid_envelope()}
        )
        assert out["_gaps_headers"]["risk_metrics"]["ingestion_authenticated"] is True
        assert out["_gaps_headers"]["metadata"]["signature_origin"] == "signed_at_ingest"
        assert not out.get("halted")

    def test_a_forged_envelope_halts_the_payload_fail_closed(self):
        out = IngestionAuthenticationModule(SECRET).process(
            {"ingestion_envelope": valid_envelope(cryptographic_signature="0" * 64)}
        )
        assert out["halted"] is True
        assert "unauthenticated" in out["block_reason"]
        assert out["_gaps_headers"]["risk_metrics"]["ingestion_authenticated"] is False

    def test_a_malformed_envelope_halts_the_payload(self):
        out = IngestionAuthenticationModule(SECRET).process(
            {"ingestion_envelope": {"body_content": ""}}
        )
        assert out["halted"] is True
        assert out["_gaps_headers"]["risk_metrics"]["ingestion_authenticated"] is False

    def test_an_already_halted_payload_is_not_processed(self):
        out = IngestionAuthenticationModule(SECRET).process(
            {"halted": True, "ingestion_envelope": valid_envelope()}
        )
        assert "_gaps_headers" not in out

    def test_the_module_carries_the_registration_marker(self):
        assert IngestionAuthenticationModule._is_authenticated_module is True
