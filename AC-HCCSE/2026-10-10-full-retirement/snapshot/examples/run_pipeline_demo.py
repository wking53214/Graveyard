"""
The original artifact's scenario, run through the rebuilt pipeline.

Prints the batch report and the routing scores, then shows the two things the
original could not: which processor actually wins the routing decision, and a
reproducible review sample.
"""

from ac_hccse import InteractionRecord, OrchestrationSystem

RECORDS = [
    InteractionRecord("id_01", "source_alpha", "proc_alpha", "Description text block A", 120, 0, True),
    InteractionRecord("id_02", "source_beta", "proc_beta", "Description text block B", 900, 4, False),
    InteractionRecord("id_03", "source_gamma", "proc_gamma", "Description text block C", 450, 2, False),
]
WORKLOAD = {"proc_alpha": 1, "proc_beta": 5, "proc_gamma": 2}
HISTORY = {"proc_alpha": [], "proc_beta": ["source_gamma"], "proc_gamma": []}


def main() -> None:
    system = OrchestrationSystem(sample_seed=42)

    evaluated = system.process_records(RECORDS)
    print("=== SCORED INTERACTIONS ===")
    for item in evaluated:
        print(f"  {item.record_id}  {item.category.value:<6} {item.evaluation_metadata}")

    group = system.new_group("group_omega", ["proc_alpha", "proc_beta", "proc_gamma"])
    report = system.execute_group_compilation(group, evaluated)
    print("\n=== BATCH REPORT ===")
    for key, value in report.items():
        print(f"  {key}: {value}")

    scores = system.allocator.calculate_priority(WORKLOAD, HISTORY, "source_gamma")
    chosen = system.route_next(WORKLOAD, HISTORY, "source_gamma")
    print("\n=== ROUTING (source_gamma) ===")
    for processor_id, score in sorted(scores.items()):
        marker = "  <-- selected" if processor_id == chosen else ""
        print(f"  {processor_id}: {score:.2f}{marker}")
    print(f"\n  proc_beta carries the heaviest load but is the only processor")
    print(f"  that has handled source_gamma before, and continuity outweighs")
    print(f"  capacity 0.7 to 0.3.")

    sample = system.retrieve_sample(RECORDS, 2)
    print("\n=== REVIEW SAMPLE (seed 42, reproducible) ===")
    for record in sample:
        print(f"  {record.record_id} from {record.source_id}")


if __name__ == "__main__":
    main()
