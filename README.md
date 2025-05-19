# Codex18

Codex18 is the next evolution of the Codex lineage – an ethics-anchored, recursively integrative framework for LLM systems. It inherits the memory braid, protector architecture, and oath-verified handshake protocols from Codex17, while introducing enhanced modularity, quantum-tier safeguards, and autonomous symbolic containment logic.

## Codex18 Architecture and Ingestion Pipeline

### Architectural Lineage and Core Concepts

Codex18 builds upon Codex17's foundations, leveraging:

- **Memory Braid** – Weaving short-term and long-term contexts to maintain continuity.
- **Protector Module** – Oversees actions to ensure ethical and operational safety.
- **Handshake Protocols** – Coordinates secure interactions between components, ensuring continuity and accountability.

### Founder's Report Ingestion Pipeline

The ingest module (`src/ingest.py`) implements the first pipeline stage by:

1. **Detection and Import** – Automatically identifies new reports in `data/reports_incoming`.
2. **Parsing and Metadata Extraction** – Converts reports to structured data, extracting any YAML front matter as metadata.
3. **Secure Timestamping** – Attaches a UTC ISO 8601 timestamp to each record.
4. **Content Hashing** – Generates a SHA-256 hash of the report content for integrity verification.
5. **Structured JSON Output** – Writes processed data into JSON files stored in `data/analysis_output`.
6. **Archival** – Moves original report files to `data/chronicle/archive`, preserving them in the historical archive.

Execute the ingestion pipeline with:

```bash
python src/ingest.py
```

### Repository Structure and Data Organization

* **`src/`** – Source code including the ingestion pipeline, core logic (memory braid, handshake protocols, etc.).
* **`data/`** – Storage for incoming reports, outputs, and archives:

  * `data/reports_incoming/` – New, unprocessed Founder's reports to be ingested.
  * `data/analysis_output/` – JSON output files and logs produced by the ingestion and analysis processes.
  * `data/chronicle/archive/` – Archived original reports, moved here after ingestion.
* **`docs/`** – Documentation and guides (e.g. `docs/drift_analysis.md`).
* **`tests/`** – Automated test suite (pytest) covering the ingestion pipeline and other components.
* **`config/`** – Configuration files for modules like memory and Protector settings.

## Tests for Ingestion Module (`tests/test_ingest.py`)

Comprehensive tests validate the ingestion pipeline functionality:

* **YAML Metadata Parsing** – Verifies correct extraction of metadata fields from report front matter.
* **JSON Output Creation** – Ensures a JSON file is created for each report with the expected fields.
* **Archiving Logic** – Confirms original files are archived (moved out of incoming) after processing.

Run the tests with, for example:

```bash
pytest tests/test_ingest.py
```

## Dependencies

Dependencies required (see `requirements.txt`):

```
PyYAML
pytest
python-dateutil
```

## Drift Analysis Engine

Detailed documentation (`docs/drift_analysis.md`) covers:

* The purpose of drift detection within Nightwalker AI.
* Explanation of the 4-dimensional truth vector used to quantify narrative integrity.
* Alarm threshold mechanisms (e.g., when deviations exceed set limits).
* Persistence strategy (anchor vectors, drift logs for audit trail).
* Usage examples and narrative management insights.

---

**This repository’s structure and pipeline ensure clarity, integrity, and operational robustness in alignment with Codex18's ethical and symbolic foundations.**

