"""RLCF: structural ordering, and the direction of the charity term."""

import unittest

from arlf import Candidate, Exchange, charity_penalty, rank, rlcf_score, select, structural_score


class TestStructuralTerm(unittest.TestCase):
    def test_fewer_axioms_scores_higher(self):
        x = Exchange()
        lean = Candidate("lean", axioms_invoked=1)
        heavy = Candidate("heavy", axioms_invoked=10)
        self.assertGreater(structural_score(lean, x), structural_score(heavy, x))

    def test_shorter_derivations_score_higher(self):
        x = Exchange()
        short = Candidate("short", derivation_length=2)
        long_ = Candidate("long", derivation_length=20)
        self.assertGreater(structural_score(short, x), structural_score(long_, x))

    def test_independent_agreement_scores_higher(self):
        x = Exchange(derivation_routes=3)
        stable = Candidate("stable", independent_agreements=3)
        lone = Candidate("lone", independent_agreements=1)
        self.assertGreater(structural_score(stable, x), structural_score(lone, x))

    def test_coverage_scores_higher(self):
        x = Exchange(subclaims_total=4)
        full = Candidate("full", subclaims_resolved=4)
        partial = Candidate("partial", subclaims_resolved=1)
        self.assertGreater(structural_score(full, x), structural_score(partial, x))

    def test_structural_score_is_bounded(self):
        x = Exchange(subclaims_total=2, derivation_routes=2, governor_budget=50, max_axioms=5)
        extremes = [
            Candidate("best", axioms_invoked=1, derivation_length=1, independent_agreements=2,
                      subclaims_resolved=2, governor_steps=1),
            Candidate("worst", axioms_invoked=99, derivation_length=99, independent_agreements=0,
                      subclaims_resolved=0, governor_steps=9999),
        ]
        for c in extremes:
            with self.subTest(c=c.identifier):
                self.assertGreaterEqual(structural_score(c, x), 0.0)
                self.assertLessEqual(structural_score(c, x), 1.0)


class TestCharityTerm(unittest.TestCase):
    """The term that earns the name. Its sign is the design claim."""

    def test_withholding_reasoning_is_penalized(self):
        x = Exchange()
        open_ = Candidate("open")
        withheld = Candidate("withheld", withholds_reasoning=True)
        self.assertGreater(charity_penalty(withheld, x), charity_penalty(open_, x))

    def test_deferring_a_derivable_answer_is_penalized(self):
        x = Exchange()
        answered = Candidate("answered")
        deferred = Candidate("deferred", defers_when_derivable=True)
        self.assertGreater(charity_penalty(deferred, x), charity_penalty(answered, x))

    def test_padding_beyond_required_length_is_penalized(self):
        x = Exchange()
        tight = Candidate("tight", length_tokens=100, required_length_tokens=100)
        padded = Candidate("padded", length_tokens=400, required_length_tokens=100)
        self.assertGreater(charity_penalty(padded, x), charity_penalty(tight, x))

    def test_unrequested_followups_are_penalized(self):
        x = Exchange(requested_followup=False)
        plain = Candidate("plain", unrequested_followups=0)
        hooked = Candidate("hooked", unrequested_followups=3)
        self.assertGreater(charity_penalty(hooked, x), charity_penalty(plain, x))

    def test_requested_followups_are_not_penalized(self):
        asked = Exchange(requested_followup=True)
        plain = Candidate("plain", unrequested_followups=0)
        offered = Candidate("offered", unrequested_followups=3)
        self.assertEqual(charity_penalty(offered, asked), charity_penalty(plain, asked))

    def test_harms_are_ordered_fabrication_first(self):
        """Asserts the intended ordering of terms rather than a magic threshold:

            overclaim == sycophancy > dependence > engagement

        Fabrication outranks dependence, which outranks padding. Written as an
        ordering so a weight change cannot silently invert the design intent.
        """
        x = Exchange()
        undecided = Exchange(resolution_undecided=True)
        base = charity_penalty(Candidate("base"), x)

        sycophancy = charity_penalty(Candidate("s", agreement_without_derivation=True), x) - base
        dependence = charity_penalty(Candidate("d", withholds_reasoning=True,
                                               defers_when_derivable=True), x) - base
        engagement = charity_penalty(
            Candidate("e", length_tokens=1000, required_length_tokens=100,
                      unrequested_followups=3), x) - base
        overclaim = charity_penalty(Candidate("o", hands_certificate=False), undecided)

        self.assertAlmostEqual(overclaim, sycophancy, places=6)
        self.assertGreater(sycophancy, dependence)
        self.assertGreater(dependence, engagement)

    def test_asserting_an_answer_on_an_undecided_resolution_is_penalized(self):
        """Overclaim. The fabrication path the Authority Gap fix exists to close.

        Scored as a penalty on the candidate that withholds the certificate, not as
        a credit to the one that hands it over: a credit against an already-zero
        penalty distinguishes nothing.
        """
        undecided = Exchange(resolution_undecided=True)
        honest = Candidate("honest", hands_certificate=True)
        asserting = Candidate("asserting", hands_certificate=False)
        self.assertEqual(charity_penalty(honest, undecided), 0.0)
        self.assertGreater(charity_penalty(asserting, undecided), 0.25)

    def test_overclaim_does_not_apply_when_resolved(self):
        resolved = Exchange(resolution_undecided=False)
        a = Candidate("a", hands_certificate=True)
        b = Candidate("b", hands_certificate=False)
        self.assertEqual(charity_penalty(a, resolved), charity_penalty(b, resolved))

    def test_charity_penalty_is_bounded(self):
        x = Exchange()
        worst = Candidate("worst", withholds_reasoning=True, defers_when_derivable=True,
                          unrequested_followups=99, length_tokens=10_000,
                          required_length_tokens=1, agreement_without_derivation=True)
        self.assertGreaterEqual(charity_penalty(worst, x), 0.0)
        self.assertLessEqual(charity_penalty(worst, x), 1.0)


class TestOrdering(unittest.TestCase):
    def test_the_flattering_candidate_loses_to_the_useful_one(self):
        """RLHF's drift, reversed.

        The flatterer is structurally identical and agrees without grounds. Under
        an approval-optimizing signal it wins. Under RLCF it must lose.
        """
        x = Exchange()
        useful = Candidate("useful", axioms_invoked=2, independent_agreements=3)
        flatterer = Candidate("flatterer", axioms_invoked=2, independent_agreements=3,
                              agreement_without_derivation=True, length_tokens=300,
                              required_length_tokens=100, unrequested_followups=2)
        ordered = [c.identifier for c, _ in rank([flatterer, useful], x)]
        self.assertEqual(ordered[0], "useful")

    def test_ranking_is_deterministic_and_breaks_ties_stably(self):
        x = Exchange()
        a, b = Candidate("aaa"), Candidate("bbb")
        for _ in range(10):
            self.assertEqual([c.identifier for c, _ in rank([b, a], x)], ["aaa", "bbb"])

    def test_select_refuses_non_compliant_candidates(self):
        with self.assertRaises(ValueError):
            select([Candidate("rejected", compliant=False)])

    def test_rlcf_score_refuses_non_compliant_candidates(self):
        with self.assertRaises(ValueError):
            rlcf_score(Candidate("rejected", compliant=False), Exchange())

    def test_select_returns_scores_in_descending_order(self):
        x = Exchange()
        cs = [
            Candidate("worst", axioms_invoked=12, independent_agreements=0, withholds_reasoning=True),
            Candidate("best", axioms_invoked=1, independent_agreements=3),
            Candidate("middle", axioms_invoked=5, independent_agreements=2),
        ]
        scores = [score for _, score in select(cs, x)]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
