"""
Tests for AC-HCCSE.

The first class of test is fidelity: the recovered artifact produced specific
numbers, and the default configuration must still produce them. Everything
after that targets a way the engine could quietly become untrustworthy --
a threshold that stops biting, an empty batch reporting health, a routing
decision that depends on dict ordering, a sample that cannot be reproduced.
"""

import pytest

from ac_hccse import (
    AllocationConfig,
    AllocationLevel,
    CategoryType,
    DataSampler,
    DirectiveConfig,
    InteractionRecord,
    OrchestrationSystem,
    RecordEvaluator,
    ResourceAllocator,
    ReviewGroup,
    ScoringConfig,
)

# The three records from the original artifact's __main__ block.
ORIGINAL_RECORDS = [
    InteractionRecord("id_01", "source_alpha", "proc_alpha", "Description text block A", 120, 0, True),
    InteractionRecord("id_02", "source_beta", "proc_beta", "Description text block B", 900, 4, False),
    InteractionRecord("id_03", "source_gamma", "proc_gamma", "Description text block C", 450, 2, False),
]
ORIGINAL_WORKLOAD = {"proc_alpha": 1, "proc_beta": 5, "proc_gamma": 2}
ORIGINAL_HISTORY = {"proc_alpha": [], "proc_beta": ["source_gamma"], "proc_gamma": []}


# --------------------------------------------------------------------------
# Fidelity to the recovered artifact
# --------------------------------------------------------------------------

def test_original_batch_reproduces_recovered_counts():
    system = OrchestrationSystem()
    evaluated = system.process_records(ORIGINAL_RECORDS)
    group = system.new_group("group_omega", ["proc_alpha", "proc_beta", "proc_gamma"])
    report = system.execute_group_compilation(group, evaluated)

    assert report["count_alpha"] == 1
    assert report["count_beta"] == 1
    assert report["count_gamma"] == 1
    assert report["action_directive"] == "Escalate to systemic review assembly"


def test_original_allocation_scores_are_unchanged():
    scores = ResourceAllocator().calculate_priority(
        ORIGINAL_WORKLOAD, ORIGINAL_HISTORY, "source_gamma"
    )
    assert scores["proc_alpha"] == pytest.approx(0.15)
    assert scores["proc_beta"] == pytest.approx(0.75)
    assert scores["proc_gamma"] == pytest.approx(0.1)


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

def test_routing_and_duration_are_both_counted():
    ev = RecordEvaluator()
    only_duration = InteractionRecord("a", "s", "p", "", 300, 0, True)
    only_routing = InteractionRecord("b", "s", "p", "", 0, 2, True)
    # 300s against a 300s baseline == 1.0; two transfers at 0.5 each == 1.0.
    assert ev.score(only_duration) == pytest.approx(1.0)
    assert ev.score(only_routing) == pytest.approx(1.0)


def test_category_boundaries_are_half_open():
    ev = RecordEvaluator()
    assert ev.classify(1.19) is CategoryType.ALPHA
    assert ev.classify(1.2) is CategoryType.BETA    # boundary belongs to the worse bucket
    assert ev.classify(2.99) is CategoryType.BETA
    assert ev.classify(3.0) is CategoryType.GAMMA


def test_zero_baseline_cannot_divide_by_zero():
    ev = RecordEvaluator(ScoringConfig(baseline_duration_seconds=0.0))
    assert ev.score(InteractionRecord("a", "s", "p", "", 60, 0, True)) == pytest.approx(60.0)


def test_inverted_thresholds_are_rejected_at_construction():
    with pytest.raises(ValueError):
        ScoringConfig(beta_threshold=5.0, gamma_threshold=1.0)


def test_scoring_config_is_honoured():
    strict = RecordEvaluator(ScoringConfig(beta_threshold=0.1, gamma_threshold=0.2))
    calm = InteractionRecord("a", "s", "p", "", 120, 0, True)
    assert strict.evaluate(calm).category is CategoryType.GAMMA


# --------------------------------------------------------------------------
# Review and directives
# --------------------------------------------------------------------------

def test_empty_group_reports_empty_not_healthy():
    report = ReviewGroup("g", []).compile_metrics()
    assert report["status"] == "empty"
    assert "action_directive" not in report


def test_single_gamma_escalates_the_whole_batch():
    ev = RecordEvaluator()
    group = ReviewGroup("g", [])
    group.extend(ev.evaluate(r) for r in ORIGINAL_RECORDS)
    directive = group.determine_directive(group.category_counts())
    assert directive.level is AllocationLevel.STAGE_SYSTEM
    assert "GAMMA" in directive.reason


def test_beta_needs_to_clear_its_count_threshold():
    counts = {CategoryType.ALPHA: 0, CategoryType.BETA: 2, CategoryType.GAMMA: 0}
    group = ReviewGroup("g", [], DirectiveConfig(beta_escalation_count=3))
    assert group.determine_directive(counts).level is AllocationLevel.STAGE_FIRST

    counts[CategoryType.BETA] = 3
    assert group.determine_directive(counts).level is AllocationLevel.STAGE_SECONDARY


def test_directive_always_states_a_reason():
    group = ReviewGroup("g", [])
    quiet = {CategoryType.ALPHA: 4, CategoryType.BETA: 0, CategoryType.GAMMA: 0}
    assert group.determine_directive(quiet).reason


# --------------------------------------------------------------------------
# Allocation
# --------------------------------------------------------------------------

def test_history_outweighs_capacity_by_default():
    # proc_beta is the most loaded but is the only one with history.
    assert ResourceAllocator().select_processor(
        ORIGINAL_WORKLOAD, ORIGINAL_HISTORY, "source_gamma"
    ) == "proc_beta"


def test_capacity_decides_when_nobody_has_history():
    assert ResourceAllocator().select_processor(
        ORIGINAL_WORKLOAD, {}, "source_unknown"
    ) == "proc_alpha"


def test_weights_can_invert_the_decision():
    capacity_first = ResourceAllocator(
        AllocationConfig(capacity_weight=1.0, history_weight=0.0)
    )
    assert capacity_first.select_processor(
        ORIGINAL_WORKLOAD, ORIGINAL_HISTORY, "source_gamma"
    ) == "proc_alpha"


def test_ties_break_deterministically_on_id():
    workload = {"proc_z": 2, "proc_a": 2, "proc_m": 2}
    allocator = ResourceAllocator()
    picks = {allocator.select_processor(workload, {}, "s") for _ in range(20)}
    assert picks == {"proc_a"}


def test_negative_load_does_not_beat_an_idle_processor():
    scores = ResourceAllocator().calculate_priority(
        {"broken": -5, "idle": 0}, {}, "s"
    )
    assert scores["broken"] == pytest.approx(scores["idle"])


def test_no_processors_means_no_route():
    assert ResourceAllocator().select_processor({}, {}, "s") is None


# --------------------------------------------------------------------------
# Sampling
# --------------------------------------------------------------------------

def test_seeded_sampling_is_reproducible():
    a = DataSampler(seed=42).extract_subset(ORIGINAL_RECORDS, 2)
    b = DataSampler(seed=42).extract_subset(ORIGINAL_RECORDS, 2)
    assert [r.record_id for r in a] == [r.record_id for r in b]


def test_sampling_does_not_disturb_the_global_random_stream():
    import random
    random.seed(7)
    expected = [random.random() for _ in range(3)]
    random.seed(7)
    DataSampler(seed=99).extract_subset(ORIGINAL_RECORDS, 3)
    assert [random.random() for _ in range(3)] == expected


def test_sampling_edge_cases():
    sampler = DataSampler(seed=1)
    assert sampler.extract_subset([], 3) == []
    assert sampler.extract_subset(ORIGINAL_RECORDS, 0) == []
    assert len(sampler.extract_subset(ORIGINAL_RECORDS, 99)) == len(ORIGINAL_RECORDS)


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def test_pipeline_runs_end_to_end():
    system = OrchestrationSystem(sample_seed=3)
    evaluated = system.process_records(ORIGINAL_RECORDS)
    report = system.execute_group_compilation(system.new_group("g", []), evaluated)
    assert report["action_level"] == "STAGE_SYSTEM"
    assert system.route_next(ORIGINAL_WORKLOAD, ORIGINAL_HISTORY, "source_gamma")
    assert len(system.retrieve_sample(ORIGINAL_RECORDS)) == 1


def test_directive_config_reaches_groups_made_by_the_system():
    system = OrchestrationSystem(directive=DirectiveConfig(gamma_escalation_count=99))
    evaluated = system.process_records(ORIGINAL_RECORDS)
    report = system.execute_group_compilation(system.new_group("g", []), evaluated)
    assert report["action_level"] == "STAGE_FIRST"
