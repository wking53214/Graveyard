from innovation_os.intelligence.system import (
    create_intelligence_system,
)


class DummyPipeline:


    def process(
        self,
        data,
        context
    ):

        return data



def test_system_bootstrap():

    system = create_intelligence_system(
        DummyPipeline()
    )


    result = system.execute(
        {
            "signal": "test"
        },
        {}
    )


    assert result["signal"] == "test"


def test_system_blocks_repeated_execution_after_retry_budget():
    system = create_intelligence_system(DummyPipeline())
    context = {
        "artifact_id": "ART-RETRY",
        "branch_id": "BRANCH-RETRY",
        "evidence_id": "EVIDENCE-RETRY",
        "evidence_version": "v1",
        "decision_state": "REJECTED",
    }

    for _ in range(3):
        assert system.execute({"signal": "repeat"}, context)["signal"] == "repeat"

    try:
        system.execute({"signal": "repeat"}, context)
    except RuntimeError as error:
        assert "Retry budget exhausted" in str(error)
    else:
        raise AssertionError("Expected repeated execution to be blocked")


def test_system_allows_reentry_after_evidence_changes():
    system = create_intelligence_system(DummyPipeline())
    base_context = {
        "artifact_id": "ART-REENTRY",
        "branch_id": "BRANCH-REENTRY",
        "evidence_id": "EVIDENCE-REENTRY",
        "decision_state": "REJECTED",
    }

    system.execute({"signal": "repeat"}, {**base_context, "evidence_version": "v1"})
    result = system.execute(
        {"signal": "repeat"},
        {**base_context, "evidence_version": "v2"},
    )

    assert result["signal"] == "repeat"
