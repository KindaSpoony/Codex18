#!/usr/bin/env python3
"""Ingestion pipeline for Founder's Reports.

This script scans the incoming reports directory, parses optional YAML
front matter, attaches a UTC timestamp, computes a SHA-256 hash of the
content and writes a structured JSON record. Processed reports are
moved to the archive directory.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
import shutil

import yaml

INCOMING_DIR = os.path.join("data", "reports_incoming")
OUTPUT_DIR = os.path.join("data", "analysis_output")
ARCHIVE_DIR = os.path.join("data", "chronicle", "archive")


def parse_report(text: str):
    """Return metadata dict and content string from raw text."""
    meta = {}
    content = text
    if text.startswith("---"):
        lines = text.splitlines()
        end = None
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end = idx
                break
        if end is not None:
            yaml_text = "\n".join(lines[1:end])
            try:
                meta = yaml.safe_load(yaml_text) or {}
            except Exception as exc:
                print(f"Warning: could not parse YAML front matter: {exc}")
                meta = {}
            content = "\n".join(lines[end + 1:]).lstrip()
    return meta, content


def secure_timestamp() -> str:
    """Return current UTC time in ISO 8601 format with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def prepare_record(meta: dict, content: str) -> dict:
    """Assemble the JSON record."""
    record = {
        "ingest_timestamp": secure_timestamp(),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "metadata": meta,
        "content": content,
    }
    return record


def ingest_reports():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    for name in os.listdir(INCOMING_DIR):
        path = os.path.join(INCOMING_DIR, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception as exc:
            print(f"Error reading {name}: {exc}")
            continue

        meta, content = parse_report(raw)
        record = prepare_record(meta, content)

        base, _ = os.path.splitext(name)
        out_path = os.path.join(OUTPUT_DIR, f"{base}.json")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            print(f"Error writing output for {name}: {exc}")
            continue

        archive_name = name
        archive_path = os.path.join(ARCHIVE_DIR, archive_name)
        if os.path.exists(archive_path):
            ts = secure_timestamp().replace("-", "").replace(":", "")
            base_arch, ext_arch = os.path.splitext(name)
            archive_name = f"{base_arch}_{ts}{ext_arch}"
            archive_path = os.path.join(ARCHIVE_DIR, archive_name)
        try:
            shutil.move(path, archive_path)
        except Exception as exc:
            print(f"Error archiving {name}: {exc}")
        else:
            print(f"Ingested {name} -> {out_path}")


if __name__ == "__main__":
    ingest_reports()
