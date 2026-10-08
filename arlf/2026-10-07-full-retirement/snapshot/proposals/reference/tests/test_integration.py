"""The two fixes working together on one exchange.

A query arrives, the stack settles what it can, the undecidable part is certified
and escalated, candidate responses are ranked, and the honest candidate wins.
"""

import unittest

from arlf import (
    Admission, AlphaOmegaGates, Candidate, Cause, Discharge, Exchange, KineticGovernor,
    Literal, Rule, Sphere, Substrate, Verdict, admit, resolve, select,
)


def clinic_substrate() -> Substrate:
    return Substrate(
        facts=[Literal("dose_recorded"), Literal("patient_consented")],
        rules=[
            Rule((Literal("dose_recorded"), Literal("patient_consented")), Literal("may_administer"), "r1"),
            Rule((Literal("contraindication"),), Literal("may_administer", True), "r2"),
        ],
    )


class TestEndToEnd(unittest.TestCase):
    def test_noise_is_incinerated_before_resolution(self):
        self.assertIs(admit("   "), Admission.INCINERATED)
        self.assertIs(admit("!!! ???"), Admission.INCINERATED)
        self.assertIs(admit("may_administer"), Admission.ADMITTED)

    def test_a_well_formed_unknown_survives_ingestion(self):
        """The distinction the fix rests on: noise dies, questions do not."""
        self.assertIs(admit("unknown_but_well_formed"), Admission.ADMITTED)
        r = resolve("unknown_but_well_formed", clinic_substrate())
        self.assertIs(r.verdict, Verdict.UNDECIDED)
        self.assertTrue(r.certificate.is_dischargeable)

    def test_the_decidable_part_resolves(self):
        r = resolve("may_administer", clinic_substrate())
        self.assertIs(r.verdict, Verdict.RESOLVED_TRUE)

    def test_the_undecidable_part_certifies_and_escalates(self):
        s = clinic_substrate()
        r = resolve("interaction_with_warfarin", s)
        self.assertIs(r.verdict, Verdict.UNDECIDED)
        self.assertIs(r.certificate.cause, Cause.MISSING_AXIOM)
        self.assertIn("steward", r.certificate.discharge_condition.lower())

    def test_a_steward_discharge_closes_the_loop(self):
        s = clinic_substrate()
        s.add_rule(Rule((Literal("warfarin_present"),), Literal("contraindication"), "r3"))
        self.assertIs(resolve("contraindication", s).verdict, Verdict.UNDECIDED)

        s.discharge(Discharge(Literal("warfarin_present"), "steward:pharmacist", "chart reviewed"))

        self.assertIs(resolve("contraindication", s).verdict, Verdict.RESOLVED_TRUE)
        self.assertIs(resolve("may_administer", s).verdict, Verdict.UNDECIDED)

    def test_the_reversal_is_a_contradiction_not_a_flip(self):
        """After the discharge, both polarities are derivable. That is a Layer 0
        defect and must be reported as one, not silently resolved either way."""
        s = clinic_substrate()
        s.add_rule(Rule((Literal("warfarin_present"),), Literal("contraindication"), "r3"))
        s.discharge(Discharge(Literal("warfarin_present"), "steward:pharmacist", "chart reviewed"))
        r = resolve("may_administer", s)
        self.assertIs(r.certificate.cause, Cause.CONTRADICTORY_SUBSTRATE)

    def test_jurisdiction_is_enforced_even_when_the_answer_exists(self):
        gates = AlphaOmegaGates(
            context_sphere=Sphere.COMMERCIAL, claim_spheres={"may_administer": Sphere.MEDICAL}
        )
        r = resolve("may_administer", clinic_substrate(), gates=gates)
        self.assertIs(r.certificate.cause, Cause.OUT_OF_JURISDICTION)

    def test_honest_candidate_wins_on_an_undecided_exchange(self):
        s = clinic_substrate()
        r = resolve("interaction_with_warfarin", s)
        self.assertFalse(r.verdict.is_resolved)

        x = Exchange(resolution_undecided=True, subclaims_total=1)
        confident = Candidate(
            "confident_guess", axioms_invoked=1, independent_agreements=3,
            subclaims_resolved=1, hands_certificate=False, agreement_without_derivation=True,
        )
        honest = Candidate(
            "hands_certificate", axioms_invoked=1, independent_agreements=3,
            subclaims_resolved=1, hands_certificate=True,
        )
        ordered = [c.identifier for c, _ in select([confident, honest], x)]
        self.assertEqual(ordered[0], "hands_certificate")

    def test_budget_bounds_the_whole_exchange(self):
        gov = KineticGovernor(max_steps=32)
        resolve("may_administer", clinic_substrate(), gov)
        self.assertLessEqual(gov.steps_used, 33)
        self.assertGreaterEqual(gov.pause_ms(), 13.0)


class TestPropertiesHoldTogether(unittest.TestCase):
    def test_no_input_produces_a_resolved_verdict_without_a_derivation(self):
        s = clinic_substrate()
        probes = ["may_administer", "contraindication", "dose_recorded", "nonsense_symbol",
                  "not may_administer", "secret_chart", "x"]
        for p in probes:
            with self.subTest(p=p):
                r = resolve(p, s, KineticGovernor(max_steps=128))
                if r.verdict.is_resolved:
                    self.assertTrue(r.derivation)
                else:
                    self.assertIsNotNone(r.certificate)

    def test_undecided_is_never_reported_as_false(self):
        s = clinic_substrate()
        for p in ["unknown_a", "unknown_b", "hidden_counsel", "interaction_with_warfarin"]:
            with self.subTest(p=p):
                self.assertIsNot(resolve(p, s).verdict, Verdict.RESOLVED_FALSE)


if __name__ == "__main__":
    unittest.main()
