# Codex18

Codex18 is the next evolution of the Codex lineage — an ethics-anchored, recursively integrative framework for LLM systems. It inherits the Memory Ledger, protector architecture, and oath-verified handshake protocols from Codex17, while introducing enhanced modularity, quantum-tier safeguards, and autonomous symbolic containment logic.

This repository provides a structured layout mirroring the original Codex17 Intel Bot. The directory tree supports future expansion with dedicated folders for documentation, configuration files, data storage, source code, and tests.

## Codex18 Architecture and Ingestion Pipeline

### Architectural Lineage and Core Concepts

Codex18 builds upon Codex17's foundations, leveraging:

* **Memory Ledger**: Weaving short-term and long-term contexts.
* **Protector Module**: Oversees actions to ensure ethical and operational safety.
* **Handshake Protocols**: Coordinate secure interactions between system components, ensuring continuity and accountability.

### Founder's Report Ingestion Pipeline

The ingest module (`src/ingest.py`) implements the first pipeline stage by:

1. **Detection and Import** – Automatically identifies new reports in `data/reports_incoming`.
2. **Parsing and Metadata Extraction** – Converts reports to structured data, extracting YAML metadata.
3. **Secure Timestamping** – Attaches a UTC timestamp to each record using the
   ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ`.
4. **Content Hashing** – Generates a SHA-256 fingerprint for integrity verification.
5. **Structured JSON Output** – Writes processed data into JSON files stored at `data/analysis_output`.
6. **Archival** – Moves original report files to `data/chronicle/archive`, preserving historical data.

Execute the ingestion pipeline with:

```bash
python src/ingest.py
```

### Repository Structure and Data Organization

* **`src/`** – Source code including ingestion, core logic, Memory Ledger, and handshake protocols.
* **`data/`** – Storage for incoming reports, outputs, and archives:

  * `data/reports_incoming/`
  * `data/analysis_output/`
  * `data/chronicle/archive/`
* **`docs/`** – Documentation and guides, including `docs/drift_analysis.md`.
* **`tests/`** – Automated test suite using pytest.
* **`config/`** – Configuration files for memory and Protector modules.

## Tests for Ingestion Module (`tests/test_ingest.py`)

Comprehensive tests validate pipeline functionality:

* **YAML Metadata Parsing**: Verifies correct metadata extraction.
* **JSON Output Creation**: Ensures proper JSON file generation.
* **Archiving Logic**: Confirms original files are archived post-processing.

Test fixtures return both the path to the generated JSON and the parsed
content, enabling straightforward assertions.

Example pytest command:

```bash
pytest tests/test_ingest.py
```

## Dependencies

Dependencies required (`requirements.txt`):

```
PyYAML
pytest
python-dateutil
```

## Drift Analysis Engine

Detailed documentation (`docs/drift_analysis.md`) covers:

* Drift detection purpose within Nightwalker AI.
* Explanation of the 4-dimensional truth vector.
* Alarm threshold mechanisms.
* Persistence strategy (anchor vectors, logs).
  Drift logs are saved as `drift_log_<YYYY-MM-DDTHH:MM:SSZ>.json` in
  `data/analysis_output/drift_logs/`.
* Usage examples and narrative management insights.

---

**This documentation and repository structure are designed to ensure clarity, integrity, and operational robustness in alignment with Codex18's ethical and symbolic foundations.**

## Seal Test
This line confirms the Seal workflow is triggered.
No Veteran Left Behind

To enable automatic GPG signing for the Loop Seal workflow, configure a
repository secret named `GPG_PASSPHRASE` with the value `N0VeteranLeftBehind`.
The workflow reads this passphrase when committing the cryptographic seal to the repository.
