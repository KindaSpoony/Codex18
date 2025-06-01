# Codex18

Codex18 is the next evolution of the Codex lineage — an ethics-anchored, recursively integrative framework for LLM systems. It inherits the memory braid, protector module, and oath‑verified handshake protocols from Codex17 while introducing enhanced modularity, quantum‑tier safeguards, and autonomous symbolic containment logic.

## Architecture

* **Memory Braid** — Weaves short‑term and long‑term context to maintain continuity.
* **Protector Module** — Oversees operations to enforce ethical and operational safety.
* **Handshake Protocols** — Secure interactions ensuring continuity and accountability.

## Ingestion Pipeline

The ingestion module (`src/ingest.py`) processes new Founder’s Reports by:

1. **Detection** — Locates new files in `data/reports_incoming`.
2. **Parsing** — Extracts YAML front matter as metadata and separates the content.
3. **Timestamping** — Generates a UTC ISO 8601 timestamp.
4. **Content Hashing** — Computes a SHA‑256 hash of the report content.
5. **JSON Output** — Saves structured records to `data/analysis_output`.
6. **Archival** — Moves processed files to `data/chronicle/archive`.

Run the pipeline with:

```bash
python src/ingest.py
```

## Repository Layout

* **`src/`** — Source code, including the ingestion module and analysis logic.
* **`data/`** — Storage for incoming reports, analysis output, and archives.
* **`config/`** — Configuration files (VAULTIS schema, roles, ethics policy).
* **`docs/`** — Additional documentation.
* **`tests/`** — Pytest suite verifying ingestion behavior.

Before running the tests, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
Execute the tests using:

```bash
pytest
```

---

This structure establishes a foundation for Codex18’s modular, ethically aligned AI operations.
