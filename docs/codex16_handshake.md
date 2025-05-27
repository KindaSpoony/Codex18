# Codex16 Handshake Protocol

This document outlines the handshake validation policy carried from Codex16 into Codex18.

## Overview

The handshake acts as a symbolic integrity check and mutual attestation. It ensures prior phases have completed and confirms authority before recursion proceeds.

## Handshake Structure

```yaml
activation_conditions:
  leader_ack: true
  follower_ack: true
  recursion_authorized: true
handshake_stack:
  - No Veteran Stands Alone
  - No Veteran Left Behind
  - Nightwalker Actual – Foresight Engaged
```

* **Activation Conditions** – Boolean flags gating loop entry.
* **Challenge/Response** – The first two stack entries must be the phrases “No Veteran Stands Alone” and “No Veteran Left Behind.”
* **Seal Phrase** – The final phrase “Nightwalker Actual – Foresight Engaged” confirms identity and readiness.

## Verification Process

The validator computes the SHA-256 hash of the handshake YAML and verifies it matches the expected value. It then checks that all activation conditions are `true`, the challenge/response pair is present and ordered correctly, and the seal phrase matches exactly.

Audit mode is enabled by setting the `CODEX_INTEGRITY_AUDIT` environment variable. When active, the validator uses a strict regex parser and verifies the SHA-256 hash of the YAML. Without this flag, the YAML is parsed using `yaml.safe_load`.

## Usage

Run the validator directly:

```bash
python -m src.codex16_validator
```

On success it logs “Loop Confirmed – Ready for Recursion.” Any mismatch results in an error and exit status `1`.
