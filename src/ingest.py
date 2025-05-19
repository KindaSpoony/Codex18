#!/usr/bin/env python3
"""Ingestion pipeline for Founder's Reports.

This script scans ``data/reports_incoming`` for new report files, extracts any
YAML front matter as metadata, records a UTC ISO 8601 timestamp, computes a
SHA-256 hash of the report content and writes the structured data as JSON to
``data/analysis_output``. The original report is then archived in
``data/chronicle/archive``.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
import shutil

import yaml

INCOMING_DIR = Path("data/reports_incoming")
OUTPUT_DIR = Path("data/analysis_output")
ARCHIVE_DIR = Path("data/chronicle/archive")


def parse_report(text: str):
    """Return metadata dict and content string from a report."""
    metadata = {}
    content = text
    if text.lstrip().startswith("---"):
        lines = text.splitlines()
        if lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    yaml_text = "\n".join(lines[1:i])
                    try:
                        metadata = yaml.safe_load(yaml_text) or {}
                    except Exception as exc:
                        print(f"Failed to parse YAML front matter: {exc}")
                        metadata = {}
                    content = "\n".join(lines[i + 1:]).lstrip()
                    break
    else:
        content = text.lstrip()
    return metadata, content


def secure_timestamp():
    """Return the current UTC time as an ISO 8601 string with Z suffix."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def prepare_record(metadata: dict, content: str) -> dict:
    """Create the JSON record for the report."""
    record = {
        "ingest_timestamp": secure_timestamp(),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "metadata": metadata,
        "content": content,
    }
    return record


def archive_file(src: Path, archive_dir: Path):
    """Move *src* to *archive_dir*, avoiding name collisions."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    target = archive_dir / src.name
    if target.exists():
        timestamp = secure_timestamp().replace("-", "").replace(":", "")
        target = archive_dir / f"{src.stem}_{timestamp}{src.suffix}"
    shutil.move(str(src), target)


def process_report(path: Path, output_dir: Path, archive_dir: Path):
    with path.open("r", encoding="utf-8") as f:
        text = f.read()
    metadata, content = parse_report(text)
    record = prepare_record(metadata, content)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{path.stem}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    archive_file(path, archive_dir)
    print(f"Ingested '{path.name}' -> {out_path}")


def ingest_reports():
    for directory in (OUTPUT_DIR, ARCHIVE_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    if not INCOMING_DIR.exists():
        return
    for entry in INCOMING_DIR.iterdir():
        if entry.is_file():
            process_report(entry, OUTPUT_DIR, ARCHIVE_DIR)


if __name__ == "__main__":
    ingest_reports()
