import json
import subprocess
import hashlib
from pathlib import Path
from dateutil import parser


def run_ingest(tmp_path: Path, fixture_name: str):
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

    script_path = Path(__file__).resolve().parents[1] / "src" / "ingest.py"
    subprocess.run(["python", str(script_path)], cwd=tmp_path, check=True)
    return incoming, output, archive, report_path.stem + ".json"


def test_yaml_metadata_parsing(tmp_path):
    incoming, output, archive, json_name = run_ingest(tmp_path, "report_with_yaml.md")
    out_file = output / json_name
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert data["metadata"].get("title") == "Test Title"
    assert data["metadata"].get("author") == "Alice Example"
    assert not (incoming / "report_with_yaml.md").exists()
    assert any(f.name.startswith("report_with_yaml") for f in archive.iterdir())


def test_json_output_file_creation(tmp_path):
    incoming, output, archive, json_name = run_ingest(tmp_path, "plain_report.txt")
    out_file = output / json_name
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert "ingest_timestamp" in data
    assert "content" in data


def test_archiving_moves_file(tmp_path):
    incoming, output, archive, _ = run_ingest(tmp_path, "plain_report.txt")
    assert not any(incoming.iterdir())
    archived_files = list(archive.iterdir())
    assert archived_files
    assert "Just some report content" in archived_files[0].read_text()


def test_content_hash_and_timestamp(tmp_path):
    incoming, output, archive, json_name = run_ingest(tmp_path, "plain_report.txt")
    out_file = output / json_name
    data = json.loads(out_file.read_text())
    expected_hash = hashlib.sha256("Just some report content".encode("utf-8")).hexdigest()
    assert data["sha256"] == expected_hash
    ts = data["ingest_timestamp"]
    dt = parser.isoparse(ts)
    assert dt.tzinfo is not None
    assert dt.utcoffset() is not None and dt.utcoffset().total_seconds() == 0
