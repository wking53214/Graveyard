"""Code-derived structural signature extractor.

Produces the raw, mechanical half of a CODE_IDENTITY_FINGERPRINT: the facts
about a source tree that can be read off the AST without running anything and
without believing anything the code says about itself.

WHAT THIS IS FOR
----------------
A system's identity is supposed to be derived from what its code does, not
from its README, its repository name, or its class names. Class names are
especially unreliable: a class called ``WorldModel`` may be three tanh layers,
and a module documented as a "cryptographic interlock" may be a SHA-256 hash
chain with no confidentiality property at all. Both of those are real examples
from this portfolio (see ``sentinel_os/sage_k/kernel.py`` and
``sentinel_os/sage_k/gsa_adapter.py``, whose docstrings say so plainly).

So this tool extracts only what is structurally checkable, and deliberately
makes no judgement:

  - class and enum names, their bases, their methods, their members
  - numeric and string constants declared at module or class level
  - the subset of those constants whose names mark them as tunables
    (threshold, limit, max, min, seed, weight, rate, window, decay, ...)
  - numeric keyword-argument defaults, which is where dataclass-style
    tunables usually hide
  - raised exception types (the fail-closed surface)
  - imported top-level packages (the dependency fingerprint)
  - textual hits for cryptographic primitives
  - textual hits for state-machine vocabulary (FROZEN, QUARANTINED,
    DEGRADED, HALF_OPEN, ...)

WHAT THIS IS NOT FOR
--------------------
It does not decide what a system *is*. That judgement is written by hand into
a fingerprint card under ``docs/fingerprints/cards/``, citing this output as
its ``[CODE]`` evidence. Keeping the mechanical step separate from the
interpretive step is the point: the mechanical step is reproducible and the
interpretive step is arguable, and conflating them is how a fingerprint
archive quietly turns into a pile of marketing copy.

It also never imports or executes the code it reads. A tree that does not even
parse still yields a record, with ``parse_error`` set -- which is itself a
finding worth keeping, since a file that raises SyntaxError on import cannot
have produced any test result anyone claims it produced.

USAGE
-----
    python tools/fingerprint/extract_signature.py <path> > signature.json

Output is JSON, one record per ``.py`` file, sorted longest-first.
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
from collections import Counter
from typing import Any

CRYPTO = re.compile(
    r"\b(hmac|hashlib|sha256|sha512|md5|blake2|secrets|cryptography|fernet"
    r"|rsa|ecdsa|nacl|pbkdf2|hkdf|signature|signing|nonce)\b",
    re.I,
)

# State-machine vocabulary. Presence of these words is a hint about the
# system's operating states, not proof that a state machine exists.
STATEWORD = re.compile(
    r"\b(FROZEN|QUARANTIN\w*|DEGRADED|FAIL_?CLOSED|FAIL_?OPEN|ESCALAT\w*"
    r"|RECOVER\w*|BREACH\w*|HALT\w*|LOCKED|SEALED|REJECTED|ACCEPTED|PENDING"
    r"|APPROVED|SUSPEND\w*|TRIPPED|OPEN|CLOSED|HALF_OPEN)\b"
)

# A constant is treated as a tunable if its NAME says so. Matching on the name
# rather than the value avoids sweeping up every incidental 0 and 1.
TUNABLE_NAME = re.compile(
    r"THRESHOLD|LIMIT|MAX|MIN|SEED|WEIGHT|RATE|TIMEOUT|WINDOW|DECAY|ALPHA"
    r"|BETA|EPS|TOLERANCE|QUORUM|PCT|PERCENT|CAP|FLOOR|CEIL|BUDGET|TTL"
    r"|RETRY|BACKOFF|DEPTH|SIZE",
    re.I,
)

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".tox"}

# Strings longer than this are prose or SQL, not configuration.
MAX_CONST_STR = 60


def _literal_assignments(tree: ast.AST) -> dict[str, Any]:
    """Every name assigned a bare literal, anywhere in the module."""
    out: dict[str, Any] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value = node.value
        if not isinstance(value, ast.Constant):
            continue
        if not isinstance(value.value, (int, float, bool, str)):
            continue
        if isinstance(value.value, str) and len(value.value) > MAX_CONST_STR:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                out[target.id] = value.value
            elif isinstance(target, ast.Attribute):
                out[target.attr] = value.value
    return out


def _numeric_defaults(tree: ast.AST) -> dict[str, Any]:
    """Numeric keyword defaults -- where policy values usually live."""
    out: dict[str, Any] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = node.args
        defaults = args.defaults or []
        positional = args.args[-len(defaults):] if defaults else []
        pairs = list(zip(positional, defaults))
        pairs += list(zip(args.kwonlyargs, args.kw_defaults or []))
        for arg, default in pairs:
            if isinstance(default, ast.Constant) and isinstance(
                default.value, (int, float)
            ) and not isinstance(default.value, bool):
                out.setdefault(arg.arg, default.value)
    return out


def _flattened_signature(path: str, source: str, parse_error: str) -> dict[str, Any]:
    """Best-effort structure for a source whose line breaks were destroyed.

    A "flattened" file is one whole module collapsed onto a single line, the
    signature damage of a copy-paste through a chat interface. They carry real
    content -- 10-33 KB of it in this portfolio's specimen corpus -- so
    reporting only `parse_error` throws away the evidence. The AST is
    unavailable, so this falls back to regex over the text and marks every
    field it produces as approximate.

    Two properties are worth recording because they are diagnostic:
    `wc -l` reports 0 lines while the file carries kilobytes, and a flattened
    file whose single line begins with `#` is one module-sized comment that
    imports cleanly, raises nothing, and defines nothing -- it fails an
    importability check by passing it.
    """
    commented_out = source.lstrip().startswith("#")
    return {
        "path": path,
        "lines": source.count("\n") + 1,
        "bytes": len(source),
        "parse_error": parse_error,
        "flattened": True,
        "silently_inert": commented_out,
        "approximate": True,
        "classes_approx": sorted(set(re.findall(r"\bclass\s+(\w+)", source))),
        "defs_approx": sorted(set(re.findall(r"\bdef\s+(\w+)", source))),
        "enum_members_approx": sorted(set(re.findall(r"\b([A-Z][A-Z0-9_]{2,})\s*=\s*[\"']", source))),
        "numeric_fields_approx": {
            m.group(1): m.group(2)
            for m in re.finditer(r"(\w+)\s*:\s*(?:float|int)\s*=\s*([0-9][0-9.e+\-]*)", source)
        },
        "crypto_hits": sorted({m.group(0).lower() for m in CRYPTO.finditer(source)})[:15],
        "state_words": sorted({m.group(0) for m in STATEWORD.finditer(source)})[:30],
    }


def analyze(path: str) -> dict[str, Any] | None:
    try:
        source = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None

    line_count = source.count("\n") + 1

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        # A file that does not parse cannot have produced any result
        # attributed to it -- so the error is always recorded. But a flattened
        # module still holds recoverable structure; see _flattened_signature.
        parse_error = f"{exc.msg} @line {exc.lineno}"
        if line_count <= 2 and len(source) > 500:
            return _flattened_signature(path, source, parse_error)
        return {"path": path, "lines": line_count, "parse_error": parse_error}

    classes: list[dict[str, Any]] = []
    enums: list[dict[str, Any]] = []
    func_count = 0
    async_count = 0
    decorators: Counter[str] = Counter()
    raises: Counter[str] = Counter()
    imports: Counter[str] = Counter()

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) for b in node.bases]
            entry: dict[str, Any] = {
                "name": node.name,
                "bases": bases,
                "methods": [
                    n.name for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ],
            }
            if any("Enum" in b for b in bases):
                entry["members"] = [
                    t.id for n in node.body if isinstance(n, ast.Assign)
                    for t in n.targets if isinstance(t, ast.Name)
                ]
                enums.append(entry)
            else:
                classes.append(entry)
            for dec in node.decorator_list:
                decorators[ast.unparse(dec)] += 1
        elif isinstance(node, ast.FunctionDef):
            func_count += 1
        elif isinstance(node, ast.AsyncFunctionDef):
            async_count += 1
        elif isinstance(node, ast.Raise) and node.exc is not None:
            raises[ast.unparse(node.exc).split("(")[0]] += 1
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name.split(".")[0]] += 1
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports[node.module.split(".")[0]] += 1

    consts = _literal_assignments(tree)
    thresholds = {
        name: value for name, value in consts.items()
        if TUNABLE_NAME.search(name)
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
    }

    # A file can parse cleanly and still define nothing. The case that matters
    # is a flattened module whose single line begins with `#`: Python reads the
    # whole file as one comment, so it imports without error, raises nothing,
    # and defines no names -- an importability check reports it as healthy.
    #
    # Two things a naive version of this check gets wrong, both found by
    # running it across the portfolio:
    #   - A config module that only assigns a dict (`LOAD_TEST_CONFIG = {...}`)
    #     declares something real and is imported by name elsewhere. Literal
    #     assignments count.
    #   - A docstring-only `__init__.py` is ordinary. Size alone proves nothing.
    # So `silently_inert` additionally requires the flattened single-line shape;
    # a normal multi-line file that merely opens with a comment is not this.
    # Any bound name counts, whatever its value: `LOAD_TEST_CONFIG = {...}` is
    # a real declaration that other modules import, even though the value is a
    # dict rather than a scalar literal and so never reaches `consts`.
    binds_a_name = any(
        isinstance(n, (ast.Assign, ast.AnnAssign)) for n in ast.walk(tree)
    )
    declares_nothing = not (
        classes or enums or func_count or async_count or imports or binds_a_name
    )
    inert = declares_nothing and len(source) > 500

    return {
        "path": path,
        "lines": line_count,
        "bytes": len(source),
        "inert": inert,
        "silently_inert": inert and line_count <= 2 and source.lstrip().startswith("#"),
        "module_doc": (ast.get_docstring(tree) or "")[:900],
        "classes": classes,
        "enums": enums,
        "func_count": func_count + async_count,
        "async_funcs": async_count,
        "decorators": decorators.most_common(10),
        "raises": raises.most_common(12),
        "imports": imports.most_common(25),
        "consts": dict(list(consts.items())[:60]),
        "thresholds": thresholds,
        "kwdefaults": _numeric_defaults(tree),
        "crypto_hits": sorted({m.group(0).lower() for m in CRYPTO.finditer(source)})[:15],
        "state_words": sorted({m.group(0) for m in STATEWORD.finditer(source)})[:30],
    }


def walk(root: str) -> list[dict[str, Any]]:
    if os.path.isfile(root):
        record = analyze(root)
        return [record] if record is not None else []
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".py"):
                record = analyze(os.path.join(dirpath, name))
                if record is not None:
                    results.append(record)
    results.sort(key=lambda r: -r.get("lines", 0))
    return results


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().split("USAGE")[-1].strip(), file=sys.stderr)
        return 2
    json.dump(walk(argv[1]), sys.stdout, indent=1, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
