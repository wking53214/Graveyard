from pathlib import Path

from synapsis.intelligence.intelligence_api import IntelligenceAPI


def test_analyze_project_end_to_end(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    project = tmp_path / "project"
    project.mkdir()
    (project / "module.py").write_text("import os\n\ndef hello():\n    pass\n")

    api = IntelligenceAPI(project)
    result = api.analyze_project()

    assert len(result["analysis_results"]) == 1
    assert result["analysis_results"][0]["symbols"]["functions"] == ["hello"]
    assert result["snapshot"].name.startswith("snapshot_")
    assert "summary" in result["report"].sections
