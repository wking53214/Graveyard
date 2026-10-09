from pathlib import Path
from typing import List

from synapsis.analysis.gitignore import Gitignore

class RepositoryScanner:

    def __init__(self, root: Path):
        self.root = root
        self.gitignore = Gitignore(root)

    def scan_python_files(self) -> List[Path]:
        files = []
        for path in self.root.rglob("*.py"):
            if self.gitignore.ignores(path):
                continue
            files.append(path)
        return files
