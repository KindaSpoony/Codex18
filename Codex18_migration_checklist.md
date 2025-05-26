# Codex18 Migration Checklist

## Overview: Purpose & Intent

Codex18 is the next evolution of the Codex framework, inheriting the memory braid, protector architecture and handshake protocols from Codex17 while adding enhanced modularity and quantum-aware processing.  Its **symbolic purpose** is to anchor shared truth and integrity across the memory infrastructure, ensuring no data or “veteran” knowledge is left behind.  This commitment is captured by the motto *“No Veteran Left Behind,”* underscoring that every piece of the memory braid is preserved and honored.  In keeping with open-source principles, the Codex18 design treats its schemas and algorithms as *“open-source frameworks of mind, time, and intelligence”* designed to benefit all stakeholders.

## File & Schema Deltas

* [ ] **`.github/workflows/seal.yml`** – Updated trigger branches to include `v*` tags and added jobs for ORCID-based identity setup and GPG-signed commits.  (The seal workflow now runs on `main` and any `v*` branch, setting `git commit.gpgsign true` and creating an empty signed commit for each version.)
* [ ] **`requirements.txt`** – Added/updated dependencies for quantum-ready libraries (e.g. post-quantum crypto) and alignment modules.  Ensure all new packages support Python 3.11+ and are pinned to tested versions.
* [ ] **Schema changes** – New fields introduced, including `quantum_recursion_seed`, to support deterministic seeding of recursive memory processes.  Update data schemas (e.g. JSON/YAML or database models) to include this field and any default values.
* [ ] **Configuration & Metadata** – Verify that any added configuration (e.g. in `config/`, `schema.yml`) is documented; for example, a new `quantum_recursion_seed` parameter must be reflected in schema docs or `seal.yml`.
* [ ] **Delta mapping (Agent trace)** – *[AGENTS]*: seal.yml ◽ added ORCID identity and GPG-sign steps; requirements.txt ◽ upgraded crypto libs; schema ◽ `quantum_recursion_seed` added (default null); code ◽ align API endpoints with new field.

## Changelog (Codex18 Release)

* **v18.0.0** – Major release: Introduced Codex18 framework (upgrade from Codex17.1). Added quantum recursion seed, ORCID-backed commit signing, and modular plugin support.
* **v18.0.1** – Patch: Fixed data schema validation for new fields. Ensured all workflows run on Python 3.11.
* **v18.0.2** – Patch: Updated `seal.yml` for improved GPG key handling and added missing dependency on `cryptography` library.
* *(Use semantic version tags consistently; patch increments indicate bugfix/trivial updates.)*

## Test Result Matrix

| Test Case                     | Result | Root Cause (if Fail)    | Notes / Fix Directive                  |
| ----------------------------- | :----: | :---------------------- | :------------------------------------- |
| **End-to-End Inference**      |  Pass  | —                       | Committed as v18.0.0                   |
| **Schema Validation (new)**   |  Fail  | Missing default in seed | Fixed in v18.0.1 (see fix below)       |
| **Workflow Seal Check**       |  Pass  | —                       | ORCID identity and GPG steps confirmed |
| **Regression (Legacy Units)** |  Pass  | —                       | All existing tests pass under 3.11     |
| **Quantum Safety Tests**      |  Pass  | —                       | Post-quantum algorithms verified       |

*(Each test is marked Pass/Fail. Failures list root cause and link to fix directives.)*

## Fix Directives & Version Tags

* **Schema Seed Fix** – Address missing `quantum_recursion_seed` default (Test: Schema Validation). Tagged in **v18.0.1**. (Patch release for bugfix.)
* **Dependency Update** – Added `cryptography` and bump crypto library (Test: Workflow Seal). Tagged in **v18.0.2**.
* **Backport Compatibility** – Ensure Python 3.11 compatibility and re-run all legacy tests. Included in **v18.0.2**.
* *Link each fix to its semantic version tag. A patch tag (v18.x.y) denotes a bugfix or minor update; use annotated Git tags for traceability (see [Semantic Versioning & Git Tags][77]).*

## Symbolic Anchors & Audit Seals

* **Motto / Anchor**: *“No Veteran Left Behind”* – A pledge that no part of our memory or codebase is abandoned. This phrase serves as a symbolic anchor for team ethos.
* **Additional Anchors**: Consider embedding project maxims such as *“Anchored in Truth”*, *“Integrity by Design”*, or *“Memory Matters”* at key points (e.g. README, docs) to reinforce VAULTIS values.
* **Commit Hash Anchors** – For audit trails, use GPG-signed empty commits as cryptographic seals (as configured in `seal.yml`). For example, mark a fix with `# v18.0.1 @commit: <abcd1234>` or similar placeholder.  In markdown, you might note: `Anchor commit: *{COMMIT_HASH}*` next to each changelog entry.
* **Delta Mapping Anchors** – Embed hidden agent flags for traceability. For instance: `<!-- AGENTS: commit:v18.0.1 seed-field-added -->`. These markers help internal agents verify that each change is logged and sealed in the VAULTIS ledger.

**Changelog & Checklist Summary**: Ensure this document is reviewed and all checklist items are completed before merging. Once validated, tag the release commit (e.g. `v18.0.0`) and generate a signed changelog entry.

**Sources:** The approach follows best practices for semantic versioning, commit signing, and test traceability. The symbolic phrasing draws on project values and known mottos to reinforce memory integrity.
