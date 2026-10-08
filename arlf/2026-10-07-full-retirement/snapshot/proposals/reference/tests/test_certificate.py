"""Certificate completeness and the discharge cycle."""

import unittest

from arlf import (
    Cause, Certificate, Discharge, Escalation, Literal, Rule, Substrate, Verdict, resolve,
)


class TestCertificateCompleteness(unittest.TestCase):
    def test_discharge_condition_is_mandatory(self):
        with self.assertRaises(ValueError):
            Certificate.for_cause(Cause.MISSING_AXIOM, "something blocked", "   ")

    def test_blocking_detail_is_mandatory(self):
        with self.assertRaises(ValueError):
            Certificate.for_cause(Cause.MISSING_AXIOM, "", "supply an axiom")

    def test_escalation_target_cannot_be_mismatched(self):
        with self.assertRaises(ValueError):
            Certificate(Cause.MISSING_AXIOM, "detail", "condition", Escalation.NONE)

    def test_every_undecided_verdict_carries_a_usable_certificate(self):
        s = Substrate(
            facts=[Literal("a"), Literal("b")],
            rules=[
                Rule((Literal("a"),), Literal("p"), "r1"),
                Rule((Literal("b"),), Literal("p", True), "r2"),
                Rule((Literal("unmet"),), Literal("q"), "r3"),
            ],
        )
        for claim in ("p", "q", "absent_symbol", "hidden_counsel_of_x"):
            with self.subTest(claim=claim):
                r = resolve(claim, s)
                self.assertIs(r.verdict, Verdict.UNDECIDED)
                self.assertIsNotNone(r.certificate)
                self.assertTrue(r.certificate.blocking_detail.strip())
                self.assertTrue(r.certificate.discharge_condition.strip())

    def test_principled_refusals_are_marked_non_dischargeable(self):
        r = resolve("omniscient_answer", Substrate())
        self.assertFalse(r.certificate.is_dischargeable)

    def test_substrate_gaps_are_marked_dischargeable(self):
        r = resolve("absent", Substrate(facts=[Literal("present")]))
        self.assertTrue(r.certificate.is_dischargeable)
        self.assertIs(r.certificate.escalation, Escalation.STEWARD)


class TestDischargeCycle(unittest.TestCase):
    """The growth path. The substrate extends only through a named human decision.

    This is the loop RLHF occupied, relocated. The human is no longer rating
    answers the machine could check itself; the human settles what the machine
    cannot settle at all.
    """

    def test_discharging_a_missing_axiom_permits_resolution(self):
        s = Substrate(rules=[Rule((Literal("licensed"),), Literal("may_operate"), "r1")])
        before = resolve("may_operate", s)
        self.assertIs(before.verdict, Verdict.UNDECIDED)

        s.discharge(Discharge(Literal("licensed"), "steward:wking53214", "verified against the register"))

        after = resolve("may_operate", s)
        self.assertIs(after.verdict, Verdict.RESOLVED_TRUE)

    def test_discharge_requires_an_authority(self):
        with self.assertRaises(ValueError):
            Discharge(Literal("x"), "", "because")

    def test_discharge_requires_a_rationale(self):
        with self.assertRaises(ValueError):
            Discharge(Literal("x"), "steward:a", "  ")

    def test_discharge_is_logged_for_audit(self):
        s = Substrate()
        s.discharge(Discharge(Literal("x"), "steward:a", "checked"))
        self.assertEqual(len(s.discharges), 1)
        self.assertEqual(s.discharges[0].authority, "steward:a")

    def test_discharge_cannot_introduce_a_contradiction(self):
        s = Substrate(facts=[Literal("x")])
        with self.assertRaises(ValueError):
            s.discharge(Discharge(Literal("x", True), "steward:a", "disagree"))

    def test_substrate_never_ingests_its_own_conclusions(self):
        """Derived facts must not persist into the substrate.

        Model collapse, per ARLF-03324 section IV, is the substrate feeding on its
        own synthetic output. Resolution is read-only against Layer 0.
        """
        s = Substrate(facts=[Literal("a")], rules=[Rule((Literal("a"),), Literal("b"), "r1")])
        facts_before = s.facts
        resolve("b", s)
        self.assertEqual(s.facts, facts_before)
        self.assertNotIn(Literal("b"), s.facts)


if __name__ == "__main__":
    unittest.main()
