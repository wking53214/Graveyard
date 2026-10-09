"""What this suite covers, and what it deliberately does not.

EDDP is an archive. Some of its Python is live, integrated code with a shared
contract; the rest is preserved artifacts -- earlier revisions and recovered
flattened sources -- kept for traceability rather than execution. Those two
populations warrant completely different treatment, and a suite that stayed
quiet about the difference would let anyone read "155 tests pass" as though it
covered the repository.

So the boundary is declared here rather than left implicit, and a new Python
file that lands in neither list fails this test until somebody decides which
it is.
"""

import ast
import os

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Live, integrated, and under behavioural test in this suite.
UNDER_BEHAVIOURAL_TEST = frozenset(
    {
        "eddp_pipeline.py",
        "eddp_telemetry_guardrail.py",
        "eddp_ingestion_authentication.py",
        "metric_assessment_telemetry_dispatch_adapter.py",
    }
)

# Preserved artifacts. Kept for provenance, not wired into anything, and not
# importable by name (the hyphenated filenames are part of what was preserved).
# They are checked for parseability only; asserting on their behaviour would
# claim a maintenance commitment this repository does not make.
PRESERVED_ARTIFACTS = frozenset(
    {
        "eddp-core-engine-v1.py",
        "eddp-core-engine-v2-refined.py",
        "_archive/metric_assessment_telemetry_dispatch_source_flattened.recovered.py",
        "_archive/ws3_telemetry_guardrail_source_flattened.recovered.py",
    }
)

# Test infrastructure, excluded from both populations.
INFRASTRUCTURE_PREFIXES = ("Tests/", "conftest.py")


def repository_python_files():
    found = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__"}]
        for name in filenames:
            if not name.endswith(".py"):
                continue
            relative = os.path.relpath(os.path.join(dirpath, name), REPO_ROOT)
            if relative.startswith(INFRASTRUCTURE_PREFIXES):
                continue
            found.append(relative)
    return sorted(found)


def test_the_repository_still_contains_the_files_this_suite_claims_to_cover():
    """A rename that silently drops a module out of coverage fails here."""
    present = set(repository_python_files())
    assert UNDER_BEHAVIOURAL_TEST <= present
    assert PRESERVED_ARTIFACTS <= present


def test_every_python_file_is_classified():
    """The point of the whole file: no Python in this repository is unaccounted
    for. A new module is either covered or explicitly declared an artifact."""
    classified = UNDER_BEHAVIOURAL_TEST | PRESERVED_ARTIFACTS
    unclassified = set(repository_python_files()) - classified
    assert not unclassified, (
        "these files are neither under behavioural test nor declared preserved "
        f"artifacts: {sorted(unclassified)}"
    )


@pytest.mark.parametrize("relative", sorted(UNDER_BEHAVIOURAL_TEST | PRESERVED_ARTIFACTS))
def test_every_python_file_parses(relative):
    """The weakest possible claim, made about everything. A file that will not
    parse is a finding, not a skip."""
    with open(os.path.join(REPO_ROOT, relative), encoding="utf-8") as handle:
        source = handle.read()
    ast.parse(source, filename=relative)


@pytest.mark.parametrize("relative", sorted(UNDER_BEHAVIOURAL_TEST))
def test_covered_modules_import_by_name(relative):
    """Being importable by name is the difference between the live modules and
    the preserved ones, and it is what lets them compose without adapters."""
    __import__(relative[:-3])


@pytest.mark.parametrize("relative", sorted(PRESERVED_ARTIFACTS))
def test_preserved_artifacts_are_not_reachable_by_import(relative):
    """Their filenames are not importable identifiers. That is a property of
    the archive, not an oversight, and if it ever changes somebody should
    decide whether the file has become live code."""
    module_name = os.path.basename(relative)[:-3]
    assert not module_name.isidentifier()
