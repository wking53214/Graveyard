# Archived FORTRESS files

Neither file here runs. Both have broken indentation from the original export
and were preserved rather than reconstructed by guesswork.

**predictive_state_controller_unrepaired.py** builds a state projection using
matrix operations, a different approach from the working controller in
`fortress/predictive_controller.py`. It also logs state transitions, which the
working version does not. Worth reconstructing if that approach is wanted.

**fortress_orchestrator_incomplete.py** is honestly named. It contains real
orchestration flow but references six classes that were never written.
