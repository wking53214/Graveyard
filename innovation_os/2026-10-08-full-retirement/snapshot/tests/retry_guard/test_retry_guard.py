from innovation_os.retry_guard import RetryGuardEngine


def test_same_idea_repeated_without_new_evidence_is_flagged():
    engine = RetryGuardEngine(max_retries=3)
    artifact_hash = "abc123"

    engine.register_attempt(
        "ATTEMPT-1",
        "ART-300",
        "BRANCH-300",
        "PARENT-300",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )
    engine.register_attempt(
        "ATTEMPT-2",
        "ART-300",
        "BRANCH-300",
        "PARENT-300",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )

    assert engine.assess_repetition(
        "ART-300",
        "BRANCH-300",
        "PARENT-300",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )


def test_same_idea_with_changed_evidence_is_allowed():
    engine = RetryGuardEngine(max_retries=3)
    artifact_hash = "abc123"

    engine.register_attempt(
        "ATTEMPT-3",
        "ART-301",
        "BRANCH-301",
        "PARENT-301",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )

    assert engine.allow_reentry(
        "ART-301",
        "BRANCH-301",
        "PARENT-301",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v2",
    )


def test_retry_exhaustion_is_detected():
    engine = RetryGuardEngine(max_retries=3)
    artifact_hash = "abc123"

    for index in range(3):
        engine.register_attempt(
            f"ATTEMPT-{index}",
            "ART-302",
            "BRANCH-302",
            "PARENT-302",
            "EVIDENCE-1",
            "CURRENT",
            artifact_hash,
            "v1",
        )

    assert engine.flag_oscillation(
        "ART-302",
        "BRANCH-302",
        "PARENT-302",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )


def test_new_branch_allows_reentry_without_false_positive():
    engine = RetryGuardEngine(max_retries=3)
    artifact_hash = "abc123"

    engine.register_attempt(
        "ATTEMPT-4",
        "ART-303",
        "BRANCH-303",
        "PARENT-303",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )

    assert engine.allow_reentry(
        "ART-303",
        "BRANCH-304",
        "PARENT-303",
        "EVIDENCE-1",
        "CURRENT",
        artifact_hash,
        "v1",
    )


def test_nonconsecutive_repeated_output_is_detected_as_cycle():
    engine = RetryGuardEngine(max_retries=3)
    for attempt_id, artifact_hash in (
        ("ATTEMPT-A", "hash-a"),
        ("ATTEMPT-B", "hash-b"),
        ("ATTEMPT-C", "hash-a"),
    ):
        engine.register_attempt(
            attempt_id,
            "ART-304",
            "BRANCH-304",
            "PARENT-304",
            "EVIDENCE-1",
            "CURRENT",
            artifact_hash,
            "v1",
        )

    assert engine.detect_cycle(
        "ART-304",
        "BRANCH-304",
        "PARENT-304",
        "EVIDENCE-1",
        "v1",
        "hash-a",
    )
