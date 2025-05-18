# Codex18

Codex18 is the next evolution of the Codex lineage — an ethics‑anchored, recursively integrative framework for LLM systems. It inherits the memory braid, protector architecture, and oath‑verified handshake protocols from Codex17, while introducing enhanced modularity, quantum‑tier safeguards, and autonomous symbolic containment logic.

This repository currently provides a skeleton structure mirroring the layout of the original Codex17 Intel Bot. The directory tree is prepared for future expansion and includes folders for documentation, configuration files, data storage, source code, and tests.

## Codex18 Architecture and Ingestion Pipeline

### Architectural Lineage and Core Concepts

Codex18 builds on the architectural foundations of Codex17. It uses a **memory braid** to weave short‑term and long‑term context together, a dedicated **Protector module** that oversees actions for safety, and a series of **handshake protocols** that coordinate interactions between components. Together these mechanisms provide continuity of knowledge while enforcing policy constraints and establishing an auditable trail for significant operations.

### Founder's Report Ingestion Pipeline

The ingest module under `src/` implements the first stage of the pipeline. It detects new Founder’s Reports placed in `data/reports_incoming`, extracts optional YAML metadata blocks, stamps each record with a secure UTC timestamp, writes structured JSON to `data/analysis_output`, and archives the original report in `data/chronicle/archive`.

The ingestion system processes Founder's Reports end‑to‑end:

1. **Detection and Import** – New reports added to the monitored directory are automatically detected.
2. **Parsing and Content Extraction** – Reports are converted into machine‑readable text with metadata captured.
3. **Analysis and Summarization** – The core model summarizes important points, guided by the Protector.
4. **Integration into Memory Braid** – Extracted knowledge is merged into long‑term memory so future reasoning can reference it.
5. **Validation and Handshake** – The Protector validates sources and signs off before information becomes official.
6. **Storage and Indexing** – Both raw and processed reports are archived and indexed for search.
7. **Triggering Follow‑up Actions** – Actionable items from the reports can spawn tasks or notifications after approval.

Through this pipeline, Codex18 keeps its knowledge current while maintaining safety and provenance.

### Repository Structure and Data Organization

Key directories include:

* **`/reports/founders/`** – Source and processed Founder's Reports.
* **`/ingestion/`** – Scripts for detecting and parsing new documents.
* **`/core/`** – Main agent logic and memory braid implementation.
* **`/protector/`** – The safety layer and handshake protocol code.
* **`/knowledge_base/`** or **`/data/`** – Persistent long‑term memory storage.
* **`/docs/`** – Design documents and guides.
* **Configuration Files** – Settings for memory retention, Protector rules, and ingestion parameters.

This layout clarifies responsibility for each component, ensuring new reports flow from detection through processing to searchable knowledge in a maintainable way.

*(Remaining sections of the README, such as setup instructions and contributor guidelines, are unchanged.)*
