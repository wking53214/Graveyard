"""The Authority Gap's named failure mode, and its bound.

The archive records that the rigid truth gates, meeting high-entropy data, risk
"entering an infinite 'Loop of the Absurd' because it lacks a clear protocol to
handle valid unknowns safely" (ARLF-01575).

These tests construct substrates that would loop or blow up under an unbounded
resolver, and assert that resolution terminates with a certificate instead.
"""

import time
import unittest

from arlf import Cause, KineticGovernor, Literal, Rule, Substrate, Verdict, resolve


def unbounded_chain(depth: int) -> Substrate:
    """p0 is a fact and each p_n implies p_{n+1}. The target is never reachable."""
    rules = [Rule((Literal(f"p{i}"),), Literal(f"p{i + 1}"), f"r{i}") for i in range(depth)]
    return Substrate(facts=[Literal("p0")], rules=rules)


def mutual_expansion(width: int) -> Substrate:
    """Dense fan-out: every symbol implies every later symbol."""
    rules = []
    for i in range(width):
        for j in range(i + 1, width):
            rules.append(Rule((Literal(f"q{i}"),), Literal(f"q{j}"), f"r{i}_{j}"))
    return Substrate(facts=[Literal("q0")], rules=rules)


class TestLoopTerminates(unittest.TestCase):
    def test_deep_chain_terminates_with_budget_exhausted(self):
        s = unbounded_chain(5000)
        r = resolve("unreachable_target", s, KineticGovernor(max_steps=200))
        self.assertIs(r.verdict, Verdict.UNDECIDED)
        self.assertIs(r.certificate.cause, Cause.BUDGET_EXHAUSTED)

    def test_budget_is_actually_respected(self):
        budget = 150
        gov = KineticGovernor(max_steps=budget)
        resolve("unreachable_target", unbounded_chain(5000), gov)
        self.assertLessEqual(gov.steps_used, budget + 1)

    def test_dense_substrate_terminates_quickly(self):
        started = time.monotonic()
        r = resolve("never_defined", mutual_expansion(60), KineticGovernor(max_steps=400))
        elapsed = time.monotonic() - started
        self.assertFalse(r.verdict.is_resolved)
        self.assertLess(elapsed, 2.0)

    def test_exhaustion_never_produces_a_verdict(self):
        """The failure mode being prevented: a truncated search reporting falsehood."""
        for budget in (1, 2, 5, 17, 64):
            with self.subTest(budget=budget):
                r = resolve("p4000", unbounded_chain(5000), KineticGovernor(max_steps=budget))
                self.assertIsNot(r.verdict, Verdict.RESOLVED_FALSE)
                self.assertIsNot(r.verdict, Verdict.RESOLVED_TRUE)

    def test_exhaustion_certificate_states_a_remedy(self):
        r = resolve("x", unbounded_chain(5000), KineticGovernor(max_steps=10))
        self.assertIn("budget", r.certificate.discharge_condition.lower())

    def test_a_sufficient_budget_still_resolves(self):
        """The bound must not make reachable claims unreachable."""
        s = unbounded_chain(40)
        r = resolve("p40", s, KineticGovernor(max_steps=100_000))
        self.assertIs(r.verdict, Verdict.RESOLVED_TRUE)


class TestGovernorPacing(unittest.TestCase):
    def test_pause_stays_inside_the_stated_band(self):
        for used, budget in ((0, 100), (50, 100), (100, 100), (500, 100)):
            gov = KineticGovernor(max_steps=budget)
            gov.steps_used = used
            self.assertGreaterEqual(gov.pause_ms(), 13.0)
            self.assertLessEqual(gov.pause_ms(), 200.0)

    def test_harder_derivations_earn_longer_pauses(self):
        light, heavy = KineticGovernor(max_steps=100), KineticGovernor(max_steps=100)
        light.steps_used, heavy.steps_used = 5, 95
        self.assertLess(light.pause_ms(), heavy.pause_ms())


if __name__ == "__main__":
    unittest.main()
