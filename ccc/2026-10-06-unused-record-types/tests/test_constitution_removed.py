"""Tests removed from CCC tests/test_constitution.py when these features were buried.

They rely on that file's fixtures (e.g. `fact`, `system`); restore them into it to revive.
"""


def test_inflection_keeps_detection_divergence_sensitivity_significance_separate():
    system = CCCSystem()
    point = system.detect_inflection(directions=("branched",), divergence=0.9, sensitivity=0.1, machine_weight=0.99, actor=Actor.model("model"))
    assert point.significance is None
    resolved = system.resolve_inflection(point.inflection_id, significance="material redirection", actor=Actor.human("human"), reason="human assessed significance", authorization_basis="human review")
    assert resolved.significance == "material redirection"


def test_threads_and_branches_preserve_lineage():
    system = CCCSystem()
    thread = system.create_thread(title="primary", actor=Actor.human("human"))
    branch = system.create_branch(thread.thread_id, title="deferred", actor=Actor.human("human"), deferred=True)
    assert branch.parent_thread_id == thread.thread_id
    assert branch.branch_id in system.store.threads[thread.thread_id].branch_ids
    system.return_to_branch(branch.branch_id, actor=Actor.human("human"), reason="resume deferred work")
    system.resolve_branch(branch.branch_id, actor=Actor.human("human"), reason="branch resolved")
    assert system.store.branches[branch.branch_id].status.value == "RESOLVED"


def test_simulation_preserves_input_provenance_and_shared_assumptions(fact):
    system, source = fact
    simulation = system.simulate(inputs=(source.artifact_id,), assumptions=("a",), shared_assumptions=("baseline",), trajectory=("x", "y"), counterfactual="if", output="modeled", sensitivity={"a": 0.5}, limitations=("not history",), actor=Actor.model("model"))
    assert simulation.input_provenance == ((source.artifact_id, ProvenanceStatus.USER_ESTABLISHED.value),)
    assert simulation.shared_assumptions == ("baseline",)
    with pytest.raises(ConstitutionViolation):
        system.simulation.promote_to_historical(simulation.simulation_id, actor=Actor.human("human"), reason="invalid")


def test_unknown_origin_term_cannot_be_canonical(fact):
    system, _ = fact
    unknown = system.ingest("unknown source", actor=Actor.system("system"))
    term = system.propose_term(term="unknown", definition="not canonical", actor=Actor.model("model"))
    with pytest.raises(ConstitutionViolation):
        system.canonicalize(term.term_id, actor=Actor.human("human"), source_material=(unknown.artifact_id,), reason="silent promotion", authorization_basis="human")

    canonical = system.propose_term(term="known", definition="canonical", actor=Actor.human("human"), source_material=(unknown.artifact_id,))
    with pytest.raises(ConstitutionViolation):
        system.canonicalize(canonical.term_id, actor=Actor.human("human"), source_material=(unknown.artifact_id,), reason="bad source", authorization_basis="human")
