import os

from synapsis.memory.memory_engine import MemoryEngine


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = MemoryEngine()

    engine.save("example", {"value": 42})
    loaded = engine.load("example")

    assert loaded["data"] == {"value": 42}
    assert "saved_at" in loaded


def test_list_returns_saved_keys(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = MemoryEngine()

    engine.save("first", {"a": 1})
    engine.save("second", {"b": 2})

    assert set(engine.list()) == {"first", "second"}


def test_load_missing_key_returns_none(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = MemoryEngine()

    assert engine.load("does-not-exist") is None
