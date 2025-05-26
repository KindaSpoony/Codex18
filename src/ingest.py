#!/usr/bin/env python3
"""
Ingestion pipeline for Founder's Reports in Codex18.
Scans for new reports, extracts metadata, timestamps, hashes content,
outputs structured JSON, and archives the original reports.

Timestamps are recorded in UTC using the ISO 8601 format
``YYYY-MM-DDTHH:MM:SSZ``.
"""

import os
import json
import hashlib
from datetime import datetime

try:
    import yaml  # Use PyYAML if available
except Exception:
    yaml = None
import shutil

# Define directories
INCOMING_DIR = "data/reports_incoming"
OUTPUT_DIR = "data/analysis_output"
ARCHIVE_DIR = "data/chronicle/archive"

# Ensure output and archive directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Process each new report in the incoming directory
for filename in os.listdir(INCOMING_DIR):
    file_path = os.path.join(INCOMING_DIR, filename)
    if not os.path.isfile(file_path):
        continue  # skip directories or non-files

    try:
        # Read the entire file content
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        continue

    # Initialize metadata and content
    metadata = {}
    content = text

    # Detect and parse YAML front matter (between --- markers)
    if text.strip().startswith('---'):
        lines = text.splitlines()
        if len(lines) > 0 and lines[0].strip() == '---':
            # Find the closing '---'
            end_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_idx = i
                    break
            if end_idx is not None:
                # Extract YAML front matter and parse it
                yaml_lines = lines[1:end_idx]
                yaml_text = "\n".join(yaml_lines)
                if yaml is not None:
                    try:
                        metadata = yaml.safe_load(yaml_text) or {}
                    except Exception as e:
                        print(f"Warning: Failed to parse YAML front matter in {filename}: {e}")
                        metadata = {}
                else:
                    # Simple YAML parsing fallback (key: value pairs)
                    metadata = {}
                    for line in yaml_lines:
                        if not line.strip() or line.lstrip().startswith('#'):
                            continue
                        if ':' in line:
                            key, val = line.split(':', 1)
                            metadata[key.strip()] = val.strip()
                # The rest of the file after the second '---' is the content
                content = "\n".join(lines[end_idx+1:]).lstrip()
            else:
                # No closing '---' found; treat entire content as body (no metadata)
                content = text.lstrip()  # remove any leading whitespace or newline
    else:
        # No front matter present
        content = text.lstrip()

    # Generate a secure UTC timestamp for ingestion in ISO 8601 format
    timestamp_utc = datetime.utcnow().replace(microsecond=0)
    ingest_timestamp = timestamp_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Compute SHA-256 hash of the report content (as a check for integrity or duplicates)
    content_bytes = content.encode('utf-8')
    content_hash = hashlib.sha256(content_bytes).hexdigest()

    # Prepare the structured record
    record = {
        "ingest_timestamp": ingest_timestamp,
        "sha256": content_hash,
        "metadata": metadata,
        "content": content
    }

    # Determine output file path (same base name with .json extension)
    base_name, _ = os.path.splitext(filename)
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")

    try:
        # Write the JSON record to the analysis output directory
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(record, json_file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing JSON output for {filename}: {e}")
        # If writing fails, skip archiving so it can be retried
        continue

    # Archive the original report file
    try:
        # Define archive path (add timestamp if file exists to avoid name collisions)
        archive_path = os.path.join(ARCHIVE_DIR, filename)
        if os.path.exists(archive_path):
            timestamp_tag = timestamp_utc.strftime("%Y%m%dT%H%M%SZ")
            root, ext = os.path.splitext(filename)
            archive_path = os.path.join(ARCHIVE_DIR, f"{root}_{timestamp_tag}{ext}")
        shutil.move(file_path, archive_path)
    except Exception as e:
        print(f"Error archiving file {filename}: {e}")
