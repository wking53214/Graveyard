"""Layer 0: the Static Truth Substrate, and its only growth path.

Propositional, deliberately small. The point is not expressive power; it is to
make the resolution semantics of proposals/AUTHORITY_GAP_RESOLUTION.md concrete
enough to test.

The substrate grows only by discharge: a steward answering a certificate. It
never ingests its own conclusions. That single restriction is what the archive's
reviewers asked for when they predicted model collapse from a system that "feeds
on its own synthetic outputs" (ARLF-03324, section IV).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional


@dataclass(frozen=True)
class Literal:
    """A propositional literal. `negated` carries the polarity."""

    name: str
    negated: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("literal name must be non-empty")

    @property
    def opposite(self) -> "Literal":
        return Literal(self.name, not self.negated)

    def __str__(self) -> str:
        return f"{'not ' if self.negated else ''}{self.name}"

    @classmethod
    def parse(cls, text: str) -> "Literal":
        """Parse 'p' or 'not p' / '!p'."""
        s = text.strip()
        if s.startswith("!"):
            return cls(s[1:].strip(), True)
        if s.lower().startswith("not "):
            return cls(s[4:].strip(), True)
        return cls(s, False)


@dataclass(frozen=True)
class Rule:
    """premises -> conclusion. An empty premise set makes the conclusion a fact."""

    premises: tuple[Literal, ...]
    conclusion: Literal
    label: str = ""

    def __str__(self) -> str:
        name = self.label or "rule"
        if not self.premises:
            return f"{name}: |- {self.conclusion}"
        return f"{name}: {', '.join(str(p) for p in self.premises)} |- {self.conclusion}"


@dataclass(frozen=True)
class Discharge:
    """A steward's answer to a certificate, and the only way an axiom is added.

    `authority` records who supplied it. The substrate refuses anonymous growth:
    an axiom with no named author cannot be audited, and an unauditable substrate
    is the thing Layer 0 exists to prevent.
    """

    literal: Literal
    authority: str
    rationale: str

    def __post_init__(self) -> None:
        if not self.authority.strip():
            raise ValueError("a discharge must name its authority")
        if not self.rationale.strip():
            raise ValueError("a discharge must carry a rationale")


class Substrate:
    """Facts plus rules, with a vocabulary and an audit log."""

    def __init__(self, facts: Iterable[Literal] = (), rules: Iterable[Rule] = ()) -> None:
        self._facts: set[Literal] = set(facts)
        self._rules: list[Rule] = list(rules)
        self._log: list[Discharge] = []

    @property
    def facts(self) -> frozenset[Literal]:
        return frozenset(self._facts)

    @property
    def rules(self) -> tuple[Rule, ...]:
        return tuple(self._rules)

    @property
    def discharges(self) -> tuple[Discharge, ...]:
        return tuple(self._log)

    @property
    def vocabulary(self) -> frozenset[str]:
        """Every symbol the substrate says anything about.

        A claim outside the vocabulary is MISSING_AXIOM. A claim inside it that
        closure does not settle is UNDERDETERMINED. The distinction changes who
        the certificate escalates to and what it asks for.
        """
        names = {f.name for f in self._facts}
        for rule in self._rules:
            names.add(rule.conclusion.name)
            names.update(p.name for p in rule.premises)
        return frozenset(names)

    def discharge(self, discharge: Discharge) -> None:
        """Extend the substrate with a steward-supplied axiom."""
        if discharge.literal.opposite in self._facts:
            raise ValueError(
                f"discharging {discharge.literal} would contradict an existing fact; "
                "resolve the substrate defect first"
            )
        self._facts.add(discharge.literal)
        self._log.append(discharge)

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def __iter__(self) -> Iterator[Literal]:
        return iter(self._facts)

    def __repr__(self) -> str:
        return f"Substrate(facts={len(self._facts)}, rules={len(self._rules)})"
