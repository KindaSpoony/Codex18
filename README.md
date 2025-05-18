# Codex18
Codex18 is the next evolution of the Codex lineage — an ethics-anchored, recursively integrative framework for LLM systems. It inherits the memory braid, protector architecture, and oath-verified handshake protocols from Codex17, while introducing enhanced modularity, quantum-tier safeguards, and autonomous symbolic containment logic.

This repository currently provides a skeleton structure mirroring the layout of the original Codex17 Intel Bot. The directory tree is prepared for future expansion and includes folders for documentation, configuration files, data storage, source code, and tests.

The `ingest` module under `src/` now implements the first stage of the pipeline. It detects new Founder’s Reports placed in `data/reports_incoming`, extracts optional YAML metadata blocks, stamps each record with a secure UTC timestamp, writes structured JSON to `data/analysis_output`, and archives the original report in `data/chronicle/archive`.
