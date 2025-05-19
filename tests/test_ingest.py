import json
import subprocess
from pathlib import Path


def run_ingest(tmp_path: Path, fixture_name: str):
    """Run the ingest script on a fixture report.

    Returns incoming, output, archive paths along with the generated
    JSON file path and its loaded content.
    """
    data_dir = tmp_path / "data"
    incoming = data_dir / "reports_incoming"
    output = data_dir / "analysis_output"
    archive = data_dir / "chronicle" / "archive"
    incoming.mkdir(parents=True)
    output.mkdir(parents=True)
    archive.mkdir(parents=True)

    fixture_path = Path(__file__).parent / "fixtures" / fixture_name
    report_path = incoming / fixture_path.name
    report_path.write_text(fixture_path.read_text())

    script = Path(__file__).resolve().parents[1] / "src" / "ingest.py"
    subprocess.run(["python", str(script)], cwd=tmp_path, check=True)

    out_file = output / f"{report_path.stem}.json"
    data = json.loads(out_file.read_text())
    return incoming, output, archive, out_file, data


def test_yaml_metadata_parsing(tmp_path):
    incoming, output, archive, out_file, data = run_ingest(tmp_path, "report_with_yaml.md")
    assert out_file.exists()
    assert data["metadata"].get("title") == "Test Title"
    assert data["metadata"].get("author") == "Alice Example"
    assert not (incoming / "report_with_yaml.md").exists()
    assert any(f.name.startswith("report_with_yaml") for f in archive.iterdir())


def test_json_output_file_creation(tmp_path):
    incoming, output, archive, out_file, data = run_ingest(tmp_path, "plain_report.txt")
    assert out_file.exists()
    assert "ingest_timestamp" in data
    assert "content" in data
    assert data["ingest_timestamp"].endswith("Z")


def test_archiving_moves_file(tmp_path):
    incoming, output, archive, _, _ = run_ingest(tmp_path, "plain_report.txt")
    assert not any(incoming.iterdir())
    archived_files = list(archive.iterdir())
    assert archived_files
    assert "Just some report content" in archived_files[0].read_text()

