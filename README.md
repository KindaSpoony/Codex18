# Codex18 Repository

Codex18 is the next evolution of our data analysis platform, incorporating automated data ingestion and processing for Founder's Reports. It builds on lessons learned in Codex17 and introduces a robust ingestion pipeline to streamline report analysis.

## Codex18 Architecture and Ingestion Pipeline

### Architectural Lineage and Core Concepts

Codex18 builds on the architectural foundations of Codex17. It uses a **memory braid** to weave short-term and long-term context together, a dedicated **Protector module** that oversees actions for safety, and a series of **handshake protocols** that coordinate interactions between components. Together these mechanisms provide continuity of knowledge while enforcing policy constraints and establishing an auditable trail for significant operations.

### Founder's Report Ingestion Pipeline

The ingestion system processes Founder's Reports end‑to‑end:

1. **Detection and Import** – new reports added to the monitored directory are automatically detected.
2. **Parsing and Content Extraction** – the reports are converted into machine‑readable text with metadata captured.
3. **Analysis and Summarization** – the core model summarizes important points, guided by the Protector.
4. **Integration into Memory Braid** – extracted knowledge is merged into long‑term memory so future reasoning can reference it.
5. **Validation and Handshake** – the Protector validates sources and signs off before information becomes official.
6. **Storage and Indexing** – both raw and processed reports are archived and indexed for search.
7. **Triggering Follow‑up Actions** – actionable items from the reports can spawn tasks or notifications after approval.

Through this pipeline Codex18 keeps its knowledge current while maintaining safety and provenance.

### Repository Structure and Data Organization

Key directories include:

* **`/reports/founders/`** – source and processed Founder's Reports.
* **`/ingestion/`** – scripts for detecting and parsing new documents.
* **`/core/`** – main agent logic and memory braid implementation.
* **`/protector/`** – the safety layer and handshake protocol code.
* **`/knowledge_base/`** or **`/data/`** – persistent long‑term memory storage.
* **`/docs/`** – design documents and guides.
* **Configuration Files** – settings for memory retention, Protector rules, and ingestion parameters.

This layout clarifies responsibility for each component, ensuring new reports flow from detection through processing to searchable knowledge in a maintainable way.

*(Remaining sections of the README, such as setup instructions and contributor guidelines, are unchanged.)*
