from pathlib import Path

class Gitignore:
    def __init__(self, root: Path):
        self.root = root
        self.patterns = self._load_patterns()

    def _load_patterns(self):
        gitignore = self.root / ".gitignore"
        if not gitignore.exists():
            return []

        patterns = []
        for line in gitignore.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
        return patterns

    def ignores(self, path: Path) -> bool:
        rel = path.relative_to(self.root)

        for pattern in self.patterns:
            # directory ignore
            if pattern.endswith("/") and pattern[:-1] in rel.parts:
                return True

            # simple filename match
            if rel.name == pattern:
                return True

            # wildcard match
            if "*" in pattern and rel.match(pattern):
                return True

        return False
