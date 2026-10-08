"""Command line entry point.

    python -m astgraph.cli SRC [SRC ...] -o OUTDIR

Walks the given files and directories, extracts a structural graph from each
.py file, and writes three JSONL files plus a summary. Output is sorted and
content-hashed, so re-running over unchanged input produces byte-identical
files.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List

from .extractor import extract_unit
from .model import Graph, write_jsonl


def iter_python_files(paths: List[str]) -> List[str]:
    """Expand files and directories into a sorted list of .py paths."""
    found: List[str] = []
    for path in paths:
        if os.path.isfile(path):
            found.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                # Skip the usual noise so a repo scan reports real code only.
                dirs[:] = [
                    d for d in dirs
                    if d not in {".git", "__pycache__", ".venv", "venv",
                                 "node_modules", ".mypy_cache", ".pytest_cache"}
                ]
                for name in sorted(files):
                    if name.endswith(".py"):
                        found.append(os.path.join(root, name))
    return sorted(set(found))


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="astgraph",
        description="Extract a deterministic structural graph from Python source.",
    )
    parser.add_argument("sources", nargs="+", help="files or directories to scan")
    parser.add_argument("-o", "--outdir", default="graph_out",
                        help="directory for the output files (default: graph_out)")
    parser.add_argument("--include-builtins", action="store_true",
                        help="record calls to builtins such as print and len")
    parser.add_argument("--relative-to", default=None,
                        help="strip this prefix from unit names in the output")
    return parser


def main(argv: List[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)

    files = iter_python_files(args.sources)
    if not files:
        print("no .py files found", file=sys.stderr)
        return 1

    combined = Graph()
    for path in files:
        unit = os.path.relpath(path, args.relative_to) if args.relative_to else path
        try:
            source = open(path, "r", encoding="utf-8", errors="replace").read()
        except OSError as exc:
            print(f"skipping unreadable file {path}: {exc}", file=sys.stderr)
            continue
        combined.merge(
            extract_unit(source, unit=unit, include_builtins=args.include_builtins)
        )

    os.makedirs(args.outdir, exist_ok=True)
    write_jsonl(os.path.join(args.outdir, "nodes.jsonl"), combined.sorted_nodes())
    write_jsonl(os.path.join(args.outdir, "edges.jsonl"), combined.sorted_edges())
    write_jsonl(os.path.join(args.outdir, "parse_failures.jsonl"), combined.failures)

    summary = {"files_scanned": len(files), **combined.summary()}
    with open(os.path.join(args.outdir, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)

    for key in sorted(summary):
        print(f"{key}: {summary[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
