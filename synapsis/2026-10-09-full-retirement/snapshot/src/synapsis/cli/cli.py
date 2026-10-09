import argparse
import json
from pathlib import Path

from synapsis.intelligence.intelligence_api import IntelligenceAPI
from synapsis.memory.memory_engine import MemoryEngine

def pretty(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))

def cmd_analyze(args):
    api = IntelligenceAPI(Path(args.root))
    result = api.analyze_project()

    pretty({
        "snapshot": result["snapshot"].name,
        "report_sections": list(result["report"].sections.keys()),
        "files_analyzed": len(result["analysis_results"])
    })

def cmd_memory(args):
    m = MemoryEngine()
    if args.action == "list":
        pretty({"keys": m.list()})
    elif args.action == "load":
        pretty(m.load(args.key))

def cmd_snapshot(args):
    m = MemoryEngine()
    pretty(m.load(f"snapshot_{args.name}"))

def build_parser():
    parser = argparse.ArgumentParser(description="SYNAPSIS CLI")

    parser.add_argument(
        "--root",
        type=str,
        default=str(Path.home() / "synapsis"),
        help="Project root directory"
    )

    sub = parser.add_subparsers(dest="command")

    # analyze
    p_analyze = sub.add_parser("analyze", help="Run full project analysis")
    p_analyze.set_defaults(func=cmd_analyze)

    # memory
    p_memory = sub.add_parser("memory", help="Inspect memory engine")
    p_memory.add_argument("action", choices=["list", "load"])
    p_memory.add_argument("--key", type=str, default="")
    p_memory.set_defaults(func=cmd_memory)

    # snapshot
    p_snapshot = sub.add_parser("snapshot", help="Load a snapshot")
    p_snapshot.add_argument("name", type=str)
    p_snapshot.set_defaults(func=cmd_snapshot)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
