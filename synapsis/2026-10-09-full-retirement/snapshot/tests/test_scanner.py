from synapsis.analysis.scanner import RepositoryScanner


def test_finds_python_files_recursively(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "top.py").write_text("x = 1\n")
    (tmp_path / "pkg" / "nested.py").write_text("y = 2\n")

    scanner = RepositoryScanner(tmp_path)
    found = {p.name for p in scanner.scan_python_files()}

    assert found == {"top.py", "nested.py"}


def test_respects_gitignore(tmp_path):
    (tmp_path / ".gitignore").write_text("skip.py\n")
    (tmp_path / "skip.py").write_text("x = 1\n")
    (tmp_path / "keep.py").write_text("y = 2\n")

    scanner = RepositoryScanner(tmp_path)
    found = {p.name for p in scanner.scan_python_files()}

    assert found == {"keep.py"}


def test_ignores_non_python_files(tmp_path):
    (tmp_path / "readme.md").write_text("# hi\n")
    (tmp_path / "code.py").write_text("x = 1\n")

    scanner = RepositoryScanner(tmp_path)
    found = {p.name for p in scanner.scan_python_files()}

    assert found == {"code.py"}
