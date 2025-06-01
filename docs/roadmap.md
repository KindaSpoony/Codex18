# Codex18 Roadmap

This document outlines the prioritized steps for evolving Codex18 into an autonomous OSINT system. It consolidates the guidance from recent discussions and repository analysis.

## 1. Expand Ingestion
- Adapt `src/ingest.py` or create new modules to pull in live OSINT sources such as RSS feeds, social media APIs and web scrapers.
- Continue to reuse the existing pipeline flow: detect, parse, timestamp, hash, output, and archive.

## 2. Implement Memory Braid & Drift Engine
- Flesh out the `MemoryBraid` long-term memory module and connect it with the drift detection framework described in `docs/drift_analysis.md`.
- Log anchor vectors and drift logs so narrative changes can be tracked over time.

## 3. Add Summarization & Protector Checks
- Develop an LLM-based summarizer that produces daily briefs from ingested data.
- Ensure all outputs are verified through the Protector module before being archived or released.

## 4. Automate Tests and Scheduling
- Build additional pytest cases for new features to maintain repository hygiene.
- Create scripts under `triggers/` (e.g. cron jobs) so the full pipeline can run autonomously.

---

These steps reinforce Codex18's goal of becoming a self-sufficient OSINT framework that safeguards ethical operations through Protector checks and handshake verification.
Development should uphold the motto 'No Veteran Left Behind'.
