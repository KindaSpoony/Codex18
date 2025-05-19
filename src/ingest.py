#!/usr/bin/env python3
"""
Ingestion pipeline for Founder's Reports in Codex18.
Scans for new reports, extracts metadata, timestamps, hashes content,
outputs structured JSON, and archives the original reports.
"""

import os
import json
import hashlib
from datetime import datetime, timezone

import yaml
import shutil

# Define directories
INCOMING_DIR = "data/reports_incoming"
OUTPUT_DIR = "data/analysis_output"
ARCHIVE_DIR = "data/chronicle/archive"

def parse_report(text):
    """Parse the raw text of a report for YAML front matter metadata."""
    metadata = {}
    content = text
    if text.strip().startswith('---'):
        lines = text.splitlines()
        if lines[0].strip() == '---':
            end_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_idx = i
                    break
            if end_idx is not None:
                yaml_text = "\n".join(lines[1:end_idx])
                try:
                    metadata = yaml.safe_load(yaml_text) or {}
                except Exception as e:
                    print(f"Warning: Failed to parse YAML front matter: {e}")
                    metadata = {}
                content = "\n".join(lines[end_idx+1:]).lstrip()
            else:
                content = text.lstrip()
    else:
        content = text.lstrip()
    return metadata, content

def secure_timestamp():
    """Generate a secure UTC timestamp in ISO 8601 format."""
    now_utc = datetime.now(timezone.utc)
    return now_utc.isoformat()

def prepare_record(metadata, content):
    """Prepare the JSON record with timestamp, SHA-256 hash, metadata, and content."""
    ts = secure_timestamp()
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    record = {
        "ingest_timestamp": ts,
        "sha256": content_hash,
        "metadata": metadata,
        "content": content,
    }
    return record

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for filename in os.listdir(INCOMING_DIR):
        file_path = os.path.join(INCOMING_DIR, filename)
        if not os.path.isfile(file_path):
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue
        metadata, content = parse_report(text)
        record = prepare_record(metadata, content)
        base, _ = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{base}.json")
        try:
            with open(output_path, 'w', encoding='utf-8') as j:
                json.dump(record, j, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error writing JSON output for {filename}: {e}")
            continue
        try:
            archive_path = os.path.join(ARCHIVE_DIR, filename)
            if os.path.exists(archive_path):
                ts_tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                base_name, ext = os.path.splitext(filename)
                archive_path = os.path.join(ARCHIVE_DIR, f"{base_name}_{ts_tag}{ext}")
            shutil.move(file_path, archive_path)
        except Exception as e:
            print(f"Error archiving file {filename}: {e}")
        else:
            print(f"Ingested '{filename}' -> {output_path}, archived original.")

if __name__ == "__main__":
    main()
