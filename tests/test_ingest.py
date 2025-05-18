from pathlib import Path

from src import ingest


def test_parse_report(tmp_path: Path):
    report = tmp_path / "report.md"
    report.write_text("""---\nmission_id: X1\nlocation: Zone\n---\nReport body""")
    result = ingest.parse_report(report)
    assert result["metadata"].get("mission_id") == "X1"
    assert "Report body" in result["body"]
