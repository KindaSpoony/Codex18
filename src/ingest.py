from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml

# Directories used by the ingestion pipeline
REPORT_DIR = Path("data/reports_incoming")
ARCHIVE_DIR = Path("data/chronicle/archive")
OUTPUT_DIR = Path("data/analysis_output")


def detect_new_reports(directory: Path = REPORT_DIR) -> List[Path]:
    """Return a list of report files awaiting ingestion."""
    if not directory.exists():
        return []
    return sorted(p for p in directory.iterdir() if p.is_file())


def parse_report(path: Path) -> Dict[str, Any]:
    """Parse metadata and body from a report file.

    Reports may optionally contain a YAML front matter block delimited by
    '---' lines at the top of the file.
    """
    text = path.read_text()
    metadata: Dict[str, Any] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            _, meta_block, body = parts[:3]
            metadata = yaml.safe_load(meta_block) or {}
    return {"metadata": metadata, "body": body}


def secure_timestamp() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def prepare_record(path: Path) -> Dict[str, Any]:
    """Prepare a structured record from a report path."""
    parsed = parse_report(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "record_id": path.stem,
        "timestamp_utc": secure_timestamp(),
        "source_path": str(path),
        "sha256": digest,
        "metadata": parsed["metadata"],
        "content": parsed["body"],
    }


def archive_report(path: Path, archive_dir: Path = ARCHIVE_DIR) -> Path:
    """Move a processed report into the archive directory."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    target = archive_dir / path.name
    shutil.move(str(path), target)
    return target


def ingest_reports(
    report_dir: Path = REPORT_DIR,
    output_dir: Path = OUTPUT_DIR,
    archive_dir: Path = ARCHIVE_DIR,
) -> List[Dict[str, Any]]:
    """Process all pending reports and archive them."""
    output_dir.mkdir(parents=True, exist_ok=True)
    processed: List[Dict[str, Any]] = []
    for report in detect_new_reports(report_dir):
        record = prepare_record(report)
        output_path = output_dir / f"{report.stem}.json"
        with output_path.open("w") as fh:
            json.dump(record, fh, indent=2)
        archive_report(report, archive_dir)
        processed.append(record)
    return processed


if __name__ == "__main__":
    ingest_reports()
