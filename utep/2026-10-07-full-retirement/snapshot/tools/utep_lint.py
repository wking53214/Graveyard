#!/usr/bin/env python3
"""Check UTEP artifacts against the framework's own rules.

    python tools/utep_lint.py [path ...]

Three checks, each derived from a rule the framework states about itself:

1. **Em dash.** ``standards/punctuation_rule.md`` calls the prohibition
   absolute and says it applies to all output, including documentation and
   generated content. This repository is generated content.

2. **Word budget.** The archive's sizing guidance: 250 to 400 words is ideal
   for a persistent instruction, 500 to 700 workable, 1,000+ has diminishing
   returns. Applied per layer, since a kernel and a gem brief have different
   budgets.

3. **Layer discipline.** A module or gem that restates kernel text is
   duplicating a rule that already applies to it, which is the overlap the
   architecture module warns about.

Exit code 1 if any error-level check fails. Warnings do not fail the run.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EM_DASH = "—"

# (label, ideal_max, hard_max) per directory.
BUDGETS = {
    "kernel": ("kernel", 700, 1200),
    "variants": ("variant", 400, 700),
    "memories": ("memory", 150, 250),
    "standards": ("standard", 200, 300),
    "core": ("core layer", 500, 800),
    "modules": ("domain module", 500, 800),
    "gems": ("gem brief", 400, 600),
    "deployments": ("deployment", 700, 1200),
}

# Sentences that belong to the kernel and should not be restated downstream.
KERNEL_PHRASES = [
    "every token must justify its existence",
    "when brevity conflicts with correctness, choose correctness",
    "higher priorities always override lower priorities",
]

LAYER_DIRS = ("modules", "gems")


def targets(argv: list[str]) -> list[Path]:
    if argv:
        out: list[Path] = []
        for a in argv:
            p = Path(a)
            out.extend(sorted(p.rglob("*")) if p.is_dir() else [p])
        return [p for p in out if p.is_file()]
    return [
        p
        for d in list(BUDGETS) + ["docs"]
        for p in sorted((ROOT / d).rglob("*"))
        if p.is_file()
    ]


def main(argv: list[str]) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in targets(argv):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT) if path.is_absolute() else path
        layer = rel.parts[0] if rel.parts else ""

        # 1. Em dash. The punctuation rule file itself must name the character
        # in order to prohibit it, so it is the one exemption.
        if EM_DASH in text and rel.name != "punctuation_rule.md":
            for i, line in enumerate(text.splitlines(), 1):
                if EM_DASH in line:
                    errors.append(f"{rel}:{i}: em dash")

        # 2. Word budget.
        if layer in BUDGETS:
            label, ideal, hard = BUDGETS[layer]
            words = len(text.split())
            if words > hard:
                errors.append(f"{rel}: {words} words exceeds the {label} hard limit of {hard}")
            elif words > ideal:
                warnings.append(f"{rel}: {words} words over the {label} target of {ideal}")

        # 3. Layer discipline.
        if layer in LAYER_DIRS:
            lowered = re.sub(r"\s+", " ", text.lower())
            for phrase in KERNEL_PHRASES:
                if phrase in lowered:
                    warnings.append(f"{rel}: restates kernel text ({phrase!r})")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error:   {e}")

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
