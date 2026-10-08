"""AUGUR is independent of CNS, and these tests hold whether or not CNS is
installed. Each one runs in a fresh interpreter in which ``cns`` is blocked
outright (``sys.modules['cns'] = None`` makes any import of it fail), so the
result does not depend on what the test environment happens to contain.

They never skip. The connected half is in ``test_cns_connector.py``.

These tests are pytest-style (they take ``tmp_path``). Run them with
``pytest``; ``python -m unittest discover`` runs only the original AUGUR tests.
"""

from __future__ import annotations

import ast
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "augur"

BLOCK = "import sys; sys.modules['cns'] = None; sys.modules['cns.gate'] = None\n"


def _run(code: str, tmp_path: Path, *, block: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", (BLOCK if block else "") + textwrap.dedent(code)],
        capture_output=True,
        text=True,
        # AUGUR appends to an audit log on every step; keep it out of the tree.
        env={
            "PYTHONPATH": str(ROOT),
            "PATH": "",
            "AUGUR_AUDIT_LOG": str(tmp_path / "audit.log"),
        },
        timeout=60,
    )


def test_augur_and_its_connector_import_with_cns_blocked(tmp_path):
    done = _run("import augur, augur.__main__, augur.cns_connector; print('ok')", tmp_path)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_importing_augur_loads_no_cns_module_at_all(tmp_path):
    """Not blocked here: if CNS is installed, importing AUGUR must still not
    pull it in. Only a connector call may."""
    done = _run(
        """
        import sys
        import augur, augur.__main__, augur.cns_connector
        loaded = sorted(m for m in sys.modules if m == 'cns' or m.startswith('cns.'))
        assert loaded == [], loaded
        print('ok')
        """,
        tmp_path,
        block=False,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_augur_still_runs_a_simulation_with_cns_blocked(tmp_path):
    done = _run(
        """
        from augur import SimulationConfig, run_simulation
        a = run_simulation(SimulationConfig(seed=42), record_history=False)
        b = run_simulation(SimulationConfig(seed=42), record_history=False)
        assert a["regime"] == "STABLE", a["regime"]
        assert a["final_state"] == b["final_state"]
        print('ok')
        """,
        tmp_path,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_the_command_line_still_runs_with_cns_blocked(tmp_path):
    done = _run(
        """
        from augur.__main__ import main
        assert main(["--seed", "42", "--steps", "3"]) == 0
        assert main(["--steps", "0"]) == 2
        print('ok')
        """,
        tmp_path,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip().endswith("ok")


def test_connector_says_what_is_missing_when_cns_is_blocked(tmp_path):
    done = _run(
        """
        from augur import SimulationConfig
        from augur.cns_connector import CnsNotInstalled, cns_available, screen_to_cns
        assert cns_available() is False
        try:
            screen_to_cns(SimulationConfig(seed=1))
        except CnsNotInstalled as exc:
            assert "pip install 'augur[cns]'" in str(exc)
            assert isinstance(exc, ImportError)
            print('ok')
        """,
        tmp_path,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_every_connector_entry_point_fails_cleanly_when_cns_is_blocked(tmp_path):
    done = _run(
        """
        from augur import SimulationConfig
        from augur.cns_connector import (
            CnsGate, CnsNotInstalled, cns_chain, scenario_digest, screen_to_cns,
            to_cns_result,
        )
        cfg = SimulationConfig(seed=1)
        calls = {
            "CnsGate": lambda: CnsGate(),
            "cns_chain": lambda: cns_chain(),
            "scenario_digest": lambda: scenario_digest(cfg),
            "to_cns_result": lambda: to_cns_result({"regime": "STABLE"}, cfg, noise_scale=4.0),
            "screen_to_cns": lambda: screen_to_cns(cfg),
        }
        for name, call in calls.items():
            try:
                call()
            except CnsNotInstalled:
                continue
            raise SystemExit(f"{name} did not raise CnsNotInstalled")
        print('ok')
        """,
        tmp_path,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def _cns_imports(tree: ast.AST) -> list[int]:
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue
        if any(n == "cns" or n.startswith("cns.") for n in names):
            lines.append(node.lineno)
    return lines


def test_no_module_in_the_package_has_an_import_statement_for_cns():
    """The connector reaches CNS through importlib, inside a function, and
    nothing else in the package names it at all."""
    offenders = {}
    for path in sorted(PACKAGE.rglob("*.py")):
        lines = _cns_imports(ast.parse(path.read_text()))
        if lines:
            offenders[str(path.relative_to(ROOT))] = lines
    assert offenders == {}


def test_the_connectors_lazy_import_is_inside_a_function():
    tree = ast.parse((PACKAGE / "cns_connector.py").read_text())
    top_level_calls = [
        node
        for stmt in tree.body
        if not isinstance(stmt, (ast.FunctionDef, ast.ClassDef))
        for node in ast.walk(stmt)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "import_module"
    ]
    assert top_level_calls == []


README = ROOT / "README.md"


def _readme_section_8() -> str:
    text = README.read_text(encoding="utf-8")
    return text[text.index("## 8. Connecting to CNS") :]


def test_the_docs_call_the_digest_tamper_evidence_and_never_tamper_proof():
    """A verdict moved onto another scenario fails GateResult.binds; nothing
    stops one being rebuilt with another digest. 'Cannot be moved' is false."""
    section = _readme_section_8()
    assert "tamper-evidence, not tamper-proofing" in section
    assert "fails `GateResult.binds`" in section
    connector = (PACKAGE / "cns_connector.py").read_text(encoding="utf-8")
    assert "tamper-evidence, not tamper-proofing" in connector
    for text in (section, connector):
        assert "cannot be moved" not in " ".join(text.lower().split())


def test_the_readme_states_what_running_a_screen_does_to_its_host():
    """The module docstring says it too, and a connected test pins that one."""
    section = _readme_section_8()
    for stated in ("reseeds", "AUGUR_RUN_ID", "augur_audit.log", "AUGUR_AUDIT_LOG"):
        assert stated in section, stated
    # A PASS judges only the last step, and the README says that is the usual
    # case and not a corner: that is the disclosure, not an edge-case footnote.
    assert "judges the last step only" in section
    assert "the usual case, not a corner" in section
    assert "pytest" in README.read_text(encoding="utf-8")  # the CNS tests' runner


def test_the_package_declares_no_runtime_dependency():
    import tomllib

    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert data["project"]["dependencies"] == []
    extras = data["project"]["optional-dependencies"]
    (cns_requirement,) = extras["cns"]
    assert cns_requirement.startswith("cns @ git+https://github.com/wking53214/cns.git@")
    assert cns_requirement.endswith("3b465dbcc1a6a4ab6f1040f93d44483196abd737")
    # The extras that were already there are left as they were.
    assert extras["predictive"] == ["numpy"]
    assert extras["dev"] == ["pytest>=8"]
