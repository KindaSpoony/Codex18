# Codex18

Codex18 represents the next stage of the Codex lineage. It integrates Codex17's memory braid, protector module and oath‑verified handshake protocols with new modular components and symbolic containment logic.

## Architecture Overview
- **Memory Braid** — Maintains continuity between short‑term and long‑term context.
- **Protector Module** — Guards operations and enforces ethical constraints.
- **Handshake Protocols** — Coordinates secure interactions among subsystems.

## Founder's Report Ingestion Pipeline
The `src/ingest.py` module processes reports placed in `data/reports_incoming` and produces structured JSON in `data/analysis_output` while archiving originals under `data/chronicle/archive`.

1. **Detection and Import** — Scan for new report files.
2. **Parsing and Metadata Extraction** — Read files and parse YAML front matter when present.
3. **Secure Timestamping** — Attach a UTC timestamp using ISO 8601 format with a `Z` suffix.
4. **Content Hashing** — Compute a SHA‑256 hash of the report content.
5. **Structured JSON Output** — Write metadata, timestamp and content to JSON files.
6. **Archival** — Move original reports to the archive directory, appending a timestamp if needed to avoid collisions.

Run the ingestion pipeline with:
```bash
python src/ingest.py
```

## Repository Layout
```
config/    – Configuration files and schemas
data/      – Incoming reports, outputs and chronicle archive
docs/      – Project documentation
src/       – Source code including the ingestion pipeline
tests/     – Pytest suite covering the ingestion module
```

## Tests
The test suite verifies YAML metadata parsing, JSON output generation, SHA‑256 hashing, timestamp format and archival behaviour.
Run tests with:
```bash
pytest
```

## Dependencies
See `requirements.txt` for package requirements (e.g. PyYAML, pytest and python‑dateutil).
