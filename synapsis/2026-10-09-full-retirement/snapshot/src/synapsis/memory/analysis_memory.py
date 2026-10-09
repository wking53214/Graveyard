from synapsis.memory.memory_engine import MemoryEngine

class AnalysisMemory:

    def __init__(self):
        self.engine = MemoryEngine()

    def save_analysis(self, results):
        self.engine.save("latest_analysis", {"results": results})

    def load_analysis(self):
        return self.engine.load("latest_analysis")
