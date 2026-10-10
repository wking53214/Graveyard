# AC-HCCSE

**Anti-Cog / Human-Centered Customer Service Engine.**

Scores completed customer interactions for *friction*, groups them for review,
and decides who should handle the next one.

This repository is a reconstruction. The original was lost; it has been rebuilt
from the source conversation preserved in the account's Gemini archive. See
`PROVENANCE.md` for where it came from and `RECONSTRUCTION.md` for what was
changed and why.

## The idea

Most of what makes a support experience bad is structural rather than
emotional. Being transferred four times is costly no matter how politely each
transfer is handled, and a system can measure that without guessing at anyone's
state of mind.

So the engine scores two signals it can actually observe — how long the
interaction ran, and how many times it was handed off — and puts them on a
shared dimensionless scale before combining them. That last part matters: if
you add raw seconds to a raw transfer count, seconds win by three orders of
magnitude and the transfer count stops affecting the outcome at all. Duration
is divided by a baseline first, so "twice as long as expected" and "two
transfers" are comparable quantities.

**Nothing here infers emotion or scores a person.** A category describes an
interaction's distance from the operational baseline. What to do about it is a
directive addressed to a human, not an action the engine takes.

## The pipeline

| Stage | Module | What it does |
|---|---|---|
| 1 | `scoring.py` | Friction score against a configurable baseline |
| 2 | `records.py` | Buckets it — ALPHA (normal), BETA (elevated), GAMMA (substantial) |
| 3 | `review.py` | Aggregates a batch and issues a directive |
| 4 | `allocation.py` | Routes the next interaction: capacity vs. continuity |
| 5 | `sampling.py` | Draws a reproducible subset for human review |
| 6 | `orchestration.py` | Runs the whole thing |

Two policy choices are worth stating plainly, because they are the whole
behaviour of the system and both are configurable:

**Escalation is asymmetric.** A single GAMMA escalates an entire batch to
systemic review, while BETA has to clear a count threshold. That is a
deliberate bias toward surfacing the severe-and-rare over the
moderate-and-common.

**Continuity outweighs capacity, 0.7 to 0.3.** Work goes to whoever has dealt
with this customer before, even when they are the busiest, because
re-explaining a problem to a new person is most of what makes an interaction go
badly. Invert the weights and the engine becomes a load balancer instead.

An empty batch reports `status: empty`, never a clean bill of health. No
evidence is not the same as no problem.

## Running it

Standard library only. `pytest` is needed for the tests and nothing else.

```bash
pip install -e .          # or add this directory to PYTHONPATH

python3 examples/run_pipeline_demo.py    # the original scenario, end to end
python3 -m pytest tests/ -q              # 22 tests
```

## Tuning it

Every weight and threshold is a dataclass field rather than a literal buried in
a method:

```python
from ac_hccse import OrchestrationSystem, ScoringConfig, AllocationConfig

system = OrchestrationSystem(
    scoring=ScoringConfig(baseline_duration_seconds=180.0, beta_threshold=0.8),
    allocation=AllocationConfig(capacity_weight=1.0, history_weight=0.0),
    sample_seed=42,
)
```

The defaults reproduce the recovered artifact's behaviour exactly, and two
tests in the suite exist solely to pin that.
