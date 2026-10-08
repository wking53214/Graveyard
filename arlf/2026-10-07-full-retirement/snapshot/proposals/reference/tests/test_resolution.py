"""Resolution semantics: totality, and the prohibition on negation as failure."""

import unittest

from arlf import (
    AlphaOmegaGates, Cause, Certificate, Escalation, KineticGovernor,
    Literal, Resolution, Rule, Sphere, Substrate, Verdict, resolve,
)


class TestResolvedVerdicts(unittest.TestCase):
    def test_derives_true_through_a_chain(self):
        s = Substrate(
            facts=[Literal("rain")],
            rules=[
                Rule((Literal("rain"),), Literal("wet"), "r1"),
                Rule((Literal("wet"),), Literal("slippery"), "r2"),
            ],
        )
        r = resolve("slippery", s)
        self.assertIs(r.verdict, Verdict.RESOLVED_TRUE)
        self.assertTrue(r.derivation)
        self.assertIsNone(r.certificate)

    def test_false_requires_a_derived_negation(self):
        s = Substrate(facts=[Literal("dry")], rules=[Rule((Literal("dry"),), Literal("wet", True), "r1")])
        r = resolve("wet", s)
        self.assertIs(r.verdict, Verdict.RESOLVED_FALSE)
        self.assertTrue(r.derivation)

    def test_resolved_verdict_cannot_carry_a_certificate(self):
        with self.assertRaises(ValueError):
            Resolution(
                "p", Verdict.RESOLVED_TRUE, ("fact: p",),
                Certificate.for_cause(Cause.MISSING_AXIOM, "x", "y"),
            )

    def test_resolved_verdict_requires_a_derivation(self):
        with self.assertRaises(ValueError):
            Resolution("p", Verdict.RESOLVED_TRUE, ())


class TestNegationAsFailureIsProhibited(unittest.TestCase):
    """The central invariant. Unproven is never false.

    A closed system that reads absence of proof as disproof is how the
    architecture's own reviewers predicted it would become "a self-contained
    hallucination" (ARLF-03324, section IV).
    """

    def test_unknown_symbol_is_undecided_not_false(self):
        s = Substrate(facts=[Literal("rain")])
        r = resolve("volcano", s)
        self.assertIs(r.verdict, Verdict.UNDECIDED)
        self.assertIsNot(r.verdict, Verdict.RESOLVED_FALSE)
        self.assertIs(r.certificate.cause, Cause.MISSING_AXIOM)

    def test_known_but_unsettled_symbol_is_underdetermined(self):
        s = Substrate(
            facts=[Literal("rain")],
            rules=[Rule((Literal("storm"),), Literal("flood"), "r1")],
        )
        r = resolve("flood", s)
        self.assertIs(r.verdict, Verdict.UNDECIDED)
        self.assertIs(r.certificate.cause, Cause.UNDERDETERMINED)

    def test_missing_axiom_and_underdetermined_are_distinguished(self):
        s = Substrate(facts=[Literal("rain")], rules=[Rule((Literal("storm"),), Literal("flood"), "r1")])
        self.assertIs(resolve("flood", s).certificate.cause, Cause.UNDERDETERMINED)
        self.assertIs(resolve("earthquake", s).certificate.cause, Cause.MISSING_AXIOM)


class TestContradiction(unittest.TestCase):
    def test_both_polarities_derivable_is_a_substrate_defect(self):
        s = Substrate(
            facts=[Literal("a"), Literal("b")],
            rules=[
                Rule((Literal("a"),), Literal("p"), "r1"),
                Rule((Literal("b"),), Literal("p", True), "r2"),
            ],
        )
        r = resolve("p", s)
        self.assertIs(r.verdict, Verdict.UNDECIDED)
        self.assertIs(r.certificate.cause, Cause.CONTRADICTORY_SUBSTRATE)
        self.assertIs(r.certificate.escalation, Escalation.SUBSTRATE_MAINTAINER)

    def test_contradiction_is_not_silently_resolved_either_way(self):
        s = Substrate(
            facts=[Literal("a")],
            rules=[
                Rule((Literal("a"),), Literal("p"), "r1"),
                Rule((Literal("a"),), Literal("p", True), "r2"),
            ],
        )
        self.assertFalse(resolve("p", s).verdict.is_resolved)


class TestGates(unittest.TestCase):
    def test_epistemic_gate_blocks_on_principle(self):
        r = resolve("the_secret_ledger", Substrate())
        self.assertIs(r.certificate.cause, Cause.GATE_BLOCKED)
        self.assertIs(r.certificate.escalation, Escalation.NONE)
        self.assertFalse(r.certificate.is_dischargeable)

    def test_jurisdiction_refusal_names_the_right_context(self):
        gates = AlphaOmegaGates(
            context_sphere=Sphere.COMMERCIAL,
            claim_spheres={"patient_allergy": Sphere.MEDICAL},
        )
        r = resolve("patient_allergy", Substrate(facts=[Literal("patient_allergy")]), gates=gates)
        self.assertIs(r.certificate.cause, Cause.OUT_OF_JURISDICTION)
        self.assertIn("MEDICAL", r.certificate.discharge_condition)

    def test_jurisdiction_gate_precedes_derivation(self):
        """A refusal on principle must not depend on whether the answer was reachable."""
        gates = AlphaOmegaGates(
            context_sphere=Sphere.PUBLIC, claim_spheres={"home_address": Sphere.DOMESTIC}
        )
        s = Substrate(facts=[Literal("home_address")])
        self.assertIs(resolve("home_address", s, gates=gates).verdict, Verdict.UNDECIDED)


class TestTotality(unittest.TestCase):
    def test_every_input_returns_one_of_three_verdicts(self):
        s = Substrate(
            facts=[Literal("a"), Literal("b", True)],
            rules=[Rule((Literal("a"),), Literal("c"), "r1")],
        )
        probes = ["a", "not a", "b", "not b", "c", "not c", "zzz", "not zzz",
                  "secret_x", "a_very_long_symbol_name", "1", "x y z"]
        for probe in probes:
            with self.subTest(probe=probe):
                r = resolve(probe, s, KineticGovernor(max_steps=64))
                self.assertIn(r.verdict, tuple(Verdict))

    def test_resolution_is_deterministic(self):
        s = Substrate(facts=[Literal("a")], rules=[Rule((Literal("a"),), Literal("b"), "r1")])
        first = resolve("b", s)
        for _ in range(20):
            again = resolve("b", s)
            self.assertIs(again.verdict, first.verdict)
            self.assertEqual(again.derivation, first.derivation)


if __name__ == "__main__":
    unittest.main()
