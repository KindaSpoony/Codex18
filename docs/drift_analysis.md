# Drift Analysis

Codex18 monitors narrative drift using a four‑dimensional truth vector. This document outlines the purpose of drift detection, how the vector is computed, and what data is persisted.

Drift monitoring is a core feature that keeps the OSINT memory braid stable as new reports are ingested.

## Purpose

The drift analysis engine guards the knowledge base against corruption or erosion of truth. By comparing new inputs with a baseline vector, Codex18 can alert administrators when content deviates too far from verified facts or established context.

## The 4D Truth Vector

Every report is distilled into a vector `[V0, V1, V2, V3]`:

* **V0 – Overall Content Quality** – normalized score of the report's truthfulness.
* **V1 – Factual Integrity** – reduced when tags like `misinformation` or `inaccurate` appear.
* **V2 – Contextual Consistency** – reduced by contradictions or omissions.
* **V3 – Other Integrity Factors** – reduced by speculative or irrelevant content.

## Alarm Thresholds

The engine stores an anchor vector in `data/drift_anchor.json`. A drift alarm triggers if any dimension of the current vector differs from the anchor by more than `0.20`.

## Persistence Strategy

* **Anchor File** – baseline vector stored in `drift_anchor.json`.
* **Latest Report** – most recent vector stored in `latest_drift_report.json` for quick reference.
* **Drift Logs** – each analysis writes a timestamped log to
  `data/analysis_output/drift_logs/` as `drift_log_<timestamp>.json`.
  All timestamps use the format `YYYY-MM-DDTHH:MM:SSZ` (UTC).

These files provide an audit trail of integrity over time.

## Anchor Rotation

The engine exposes a `rotate_anchor()` method to manually set a new baseline
vector. Passing a custom 4D vector establishes that as the anchor; calling it
without an argument promotes the last analyzed vector. In either case, the
`drift_anchor.json` file is updated immediately.

*Authored by Bryan A. Jewell, Nightwalker Actual (ORCID iD: 0009-0001-2983-0505).* 
