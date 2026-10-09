from pathlib import Path

from synapsis.analysis.gitignore import Gitignore


def test_no_gitignore_ignores_nothing(tmp_path):
    gitignore = Gitignore(tmp_path)
    assert gitignore.ignores(tmp_path / "anything.py") is False


def test_directory_pattern_is_ignored(tmp_path):
    (tmp_path / ".gitignore").write_text("venv/\n")
    (tmp_path / "venv").mkdir()
    gitignore = Gitignore(tmp_path)
    assert gitignore.ignores(tmp_path / "venv" / "lib.py") is True


def test_exact_filename_is_ignored(tmp_path):
    (tmp_path / ".gitignore").write_text("secrets.py\n")
    gitignore = Gitignore(tmp_path)
    assert gitignore.ignores(tmp_path / "secrets.py") is True


def test_wildcard_pattern_is_ignored(tmp_path):
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    gitignore = Gitignore(tmp_path)
    assert gitignore.ignores(tmp_path / "module.pyc") is True


def test_unmatched_file_is_not_ignored(tmp_path):
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    gitignore = Gitignore(tmp_path)
    assert gitignore.ignores(tmp_path / "module.py") is False


def test_comments_and_blank_lines_are_skipped(tmp_path):
    (tmp_path / ".gitignore").write_text("# comment\n\n*.pyc\n")
    gitignore = Gitignore(tmp_path)
    assert gitignore.patterns == ["*.pyc"]
