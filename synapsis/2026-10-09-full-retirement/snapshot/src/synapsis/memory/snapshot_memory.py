from synapsis.memory.memory_engine import MemoryEngine
from synapsis.models.snapshot import Snapshot

class SnapshotMemory:

    def __init__(self):
        self.engine = MemoryEngine()

    def save_snapshot(self, snapshot: Snapshot):
        self.engine.save(f"snapshot_{snapshot.name}", {
            "created_at": snapshot.created_at.isoformat(),
            "data": snapshot.data
        })

    def load_snapshot(self, name: str):
        return self.engine.load(f"snapshot_{name}")
