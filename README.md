# Codex18 – Nightwalker OSINT Intelligence Framework

## Overview and Philosophy

Codex18 is an **ethics-anchored, multi-agent OSINT framework** built under the Nightwalker AI doctrine. It is the next evolution in the Codex series, inheriting core concepts from Codex17 (such as the Memory Ledger, Protector modules, and oath-verified handshake protocols) while introducing greater modularity, advanced safeguards, and autonomous symbolic containment logic. The project’s guiding ethos – *“No Veteran Left Behind”* – reflects its commitment to memory preservation, ethical enforcement, and narrative integrity across all operations. By design, Codex18 automatically ingests open-source intelligence reports, preserves contextual memory, detects narrative drift, and applies Protector oversight to ensure all actions remain ethical and accountable.

**Key Features:**

* **Automated Intelligence Capture:** Continuously gathers and processes incoming OSINT data streams.
* **Memory Preservation:** Employs a **Memory Ledger** to weave short-term and long-term context, ensuring knowledge retention without corruption.
* **Ethics Enforcement:** A **Protector Module** oversees decisions and outputs, enforcing strict ethical and operational safety constraints.
* **Modular Architecture:** Components communicate via secure *handshake protocols* (cryptographically verified exchanges) to maintain continuity and trust between subsystems.
* **Narrative Drift Detection:** Monitors changes in narrative or factual consistency using a drift analysis engine, alerting to deviations from established truth baselines.
* **Scalable Integration:** Designed to scale across private memory vaults, live open-source streams, and GPT-powered analysis nodes, enabling deployment in diverse intelligence environments.

## System Architecture

The Codex18 system architecture is organized into distinct but interlocking modules that together form a self-regulating intelligence cycle. Major components include the ingestion pipeline, persistent memory storage, drift analysis engine, an optional LLM-based summarizer, and Protector oversight. The diagram below illustrates the high-level data flow and module interactions:

```mermaid
graph TD
    %% Data Ingestion subgraph
    subgraph "Data Ingestion"
        incoming[Incoming Reports] --> ingest[Ingestion Pipeline]
        ingest --> ledger[Memory Ledger (Structured Store)]
        ingest --> archive[Archived Reports]
    end
    %% Analysis and Memory subgraph
    subgraph "Analysis & Memory"
        ledger --> drift[Drift Analysis Engine]
        drift --> logs[Drift Logs & Alerts]
        ledger --> summarizer[LLM Summarizer]
        summarizer --> briefs[Analytical Briefs]
    end
    protector[Protector Module]
    protector -.-> ledger
    protector -.-> drift
    protector -.-> summarizer
    protector -->|Ethical Approval| briefs
```

In this architecture, **new reports** enter through the ingestion module and are converted into structured data stored in the **Memory Ledger** (a persistent knowledge base). Ingested raw files are simultaneously archived for record-keeping. The **Drift Analysis Engine** continuously compares incoming information against an anchored truth baseline; if content deviates significantly, it generates **drift logs and alerts**. A dedicated **LLM Summarizer** (integrating with GPT-4 or similar) can produce analytical briefs or daily intelligence summaries from the Memory Ledger’s contents. Overarching everything is the **Protector Module**, which monitors the system’s operations – it verifies memory integrity, checks drift assessments, and vets summarizer outputs – enforcing ethical guidelines before any intelligence output is finalized. Secure *handshake protocols* govern interactions between these components, ensuring each action or data exchange is authenticated and in compliance with the system’s oath-bound rules.

## Ingestion Pipeline

The **Founder's Report Ingestion Pipeline** (`src/ingest.py`) is the entry point for data flow. It automatically processes any new intelligence report placed into the `data/reports_incoming/` directory, performing a series of steps to ensure the data is structured, timestamped, and tamper-evident:

1. **Detection & Import:** Scans the incoming reports directory and identifies new report files.
2. **Parsing & Metadata Extraction:** Reads each report, parses any YAML front-matter metadata (demarcated by `---`), and separates it from the main content.
3. **Secure Timestamping:** Attaches a current UTC timestamp to the data record (using ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ`).
4. **Content Hashing:** Computes a SHA-256 hash of the report content for integrity verification and future duplicate detection.
5. **Structured JSON Output:** Combines the cleaned content, extracted metadata, timestamp, and hash into a structured JSON record. The JSON output is saved to `data/analysis_output/` with a filename matching the source (e.g., `Report123.json`).
6. **Archival:** Moves the original report file into the archive (`data/chronicle/archive/`), preserving the original input in a chronological store.

After setting up a new report file in the incoming folder, you can execute the ingestion process with a single command:

```bash
python src/ingest.py
```

This will process all pending reports and produce JSON output files in the analysis output directory (and archive the originals). The pipeline is idempotent and can be re-run; unprocessed files are handled, while already-archived files are ignored on subsequent runs.

## Drift Detection Engine

Codex18 features a built-in **Drift Analysis Engine** that monitors for **narrative drift** – significant deviations or inconsistencies in newly ingested intelligence compared to the established knowledge base. At its core, the engine distills each report into a **four-dimensional “truth vector”**:

* **V0 (Overall Quality):** A normalized score representing the report’s overall truthfulness or content quality.
* **V1 (Factual Integrity):** Indicates factual accuracy; this score drops if the analysis tags content as containing misinformation or errors.
* **V2 (Contextual Consistency):** Reflects how consistent the report is with prior context; contradictions or omissions lower this score.
* **V3 (Other Integrity Factors):** Captures additional integrity aspects; speculation, irrelevance, or off-topic content reduce this score.

The drift engine compares each new report’s truth vector against a **baseline anchor vector** (stored in `data/drift_anchor.json`) to detect anomalies. If any dimension deviates from the anchor by more than a threshold (default **±0.20** on any axis), a **drift alarm** is triggered. The engine then logs the event for audit:

* The report’s vector and analysis results are saved to `data/analysis_output/latest_drift_report.json` (for quick reference to the most recent analysis).
* A detailed entry is appended to the drift log archive under `data/analysis_output/drift_logs/` as a timestamped file (e.g., `drift_log_2025-05-31T13:45:00Z.json`). These JSON logs include the new vector, the difference from the anchor, and whether an alarm was activated.
* The **anchor vector** itself remains as the reference baseline. Administrators can **rotate the anchor** when needed – i.e. accept the current state as the new normal. The engine provides a `rotate_anchor()` method to either promote the latest truth vector to the anchor or set a custom baseline, updating `drift_anchor.json` accordingly.

By preserving an anchor and a log of changes, Codex18’s drift detection mechanism ensures long-term **narrative integrity**. It helps maintain the **truth continuity** of the Memory Ledger, preventing slow erosion of facts or context by alerting operators to any significant divergences in incoming intelligence.

*(For more in-depth discussion of the drift detection methodology, see the detailed [Drift Analysis documentation](docs/drift_analysis.md).)*

## Repository Structure

The repository is organized to separate core functionality, data, and documentation in a clear manner:

* **`src/`** – Source code for the main system components (ingestion pipeline, summarizer, memory ledger logic, handshake protocols, etc.).
* **`core/`** – Core framework modules (e.g. truth vector calculation, drift analysis engine). *(*Note:* Some core logic may reside under `src/` in this iteration; the structure mirrors Codex17 and is prepared for further modularization.)*
* **`data/`** – Data storage for inputs and outputs:

  * `data/reports_incoming/` – Folder to drop incoming reports to be ingested.
  * `data/analysis_output/` – Outputs of analyses (parsed JSON records, latest drift report, drift logs, summaries, etc.).
  * `data/chronicle/archive/` – Archived original reports for historical reference.
* **`docs/`** – Documentation and design notes (e.g. this README and additional guides like drift analysis, roadmap, architecture flow).
* **`tests/`** – Unit and integration tests (using `pytest`) to verify pipeline and module functionality.
* **`config/`** – Configuration files (for setting parameters such as memory ledger schema, Protector policy rules, etc.).
* **`.github/workflows/`** – Continuous integration workflows (including the **Seal** workflow for GPG signing and integrity checks).

## Installation and Dependencies

**Prerequisites:** Ensure you have **Python 3.11+** installed (for compatibility with newer language features and libraries).

To install the required dependencies, use pip with the provided requirements file:

```bash
pip install -r requirements.txt
```

Codex18 relies on the following key Python packages (see `requirements.txt` for the full list):

```text
PyYAML        # YAML parsing for report metadata
pytest        # Testing framework
python-dateutil  # Date/time parsing and handling
requests      # HTTP requests (for future OSINT data sources)
fastapi       # REST API server (for future integration)
uvicorn       # ASGI server to run FastAPI app
pydantic      # Data validation models (used with FastAPI)
python-multipart  # File upload support for FastAPI
```

*Note:* The **LLM Summarizer** module uses OpenAI’s API. If you plan to use the summarization feature, you will need to install the `openai` Python package and set the `OPENAI_API_KEY` environment variable with your API key. (This package is not included in requirements by default.)

## Usage – Running the System

With dependencies installed, you can begin using Codex18’s core features:

* **Running the Ingestion Pipeline:** Place one or more text reports (e.g., `.txt` or markdown files with optional YAML metadata front-matter) into the `data/reports_incoming/` directory. Then execute the pipeline:

  ```bash
  python src/ingest.py
  ```

  Each new report will be processed through the steps described earlier (parse, timestamp, hash, output JSON, archive). After running, check `data/analysis_output/` for the generated JSON files and `data/chronicle/archive/` to find the original files moved to the archive.

* **Running Drift Analysis:** The drift detection runs automatically as part of the continuous integration seal workflow (see below), but it can also be invoked manually or integrated into a larger application. For manual checks, you can run the drift analysis engine on the latest data by executing:

  ```bash
  python core/drift_analysis_engine.py
  ```

  Ensure that an anchor vector exists (`data/drift_anchor.json`) before running, otherwise the first run will create one. The script will output/update the `latest_drift_report.json` and log a new entry in the drift\_logs directory.

* **Using the Summarizer:** If configured with an API key, the `src/summarizer.py` module can be used to generate JSON-formatted intelligence briefs from input data. This can be invoked by importing the `Summarizer` class in a Python session or script and calling `summarizer.summarize()` with the appropriate input dictionary. *(At present, this is an optional component and may be further integrated in future updates.)*

## Testing

A suite of **pytest** tests is included to verify core functionality of the ingestion and other modules. Notably, `tests/test_ingest.py` provides comprehensive tests for the ingestion pipeline:

* **Metadata Parsing Test:** Confirms that YAML front-matter is correctly extracted into the metadata field.
* **JSON Output Test:** Ensures that running the pipeline creates the expected `.json` output with all required fields.
* **Archiving Test:** Verifies that after processing, the original report file is moved to the archive folder.

To run the test suite, execute `pytest` at the project root (or specify a test module):

```bash
pytest tests
```

For example, to run only the ingestion tests:

```bash
pytest tests/test_ingest.py -v
```

All tests should pass, indicating that the pipeline and other components are functioning as expected. It is recommended to run tests before committing changes or deploying the system, to catch any regressions early.

## Contribution Guidelines

Contributions to Codex18 are welcome and should align with the project’s principles of clarity, integrity, and ethics. We ask contributors to keep the following guidelines in mind (see [AGENTS.md](AGENTS.md) for details):

* **Testing & Stability:** **Run the test suite** (using `pytest`) before submitting any pull request or change. All ingestion and drift detection tests should pass to ensure stability of the pipeline.
* **Commit Practices:** Use clear and descriptive commit messages. When relevant, reference the core motto *“No Veteran Left Behind”* or related symbolic anchors to maintain continuity in narrative (this serves as a mnemonic and ethical touchstone in development).
* **Documentation:** Update or add documentation in the `docs/` folder for any significant feature changes or additions. Maintaining up-to-date docs (architecture descriptions, usage instructions, etc.) is crucial for transparency.
* **Data Handling:** Avoid committing large or sensitive data. Use only minimal example data in `data/` for testing purposes, and never include any private or classified information.
* **Ethical Alignment:** Ensure that new code or modules uphold the ethical safeguards of the framework. For example, if introducing an action or decision-making component, it should integrate with the Protector module or otherwise enforce the project’s ethical constraints.

Before contributing, you might also review the architectural notes and design principles to understand the project’s direction. All contributions will be reviewed for compliance with the above guidelines and the overall Nightwalker doctrine.

## Roadmap

Codex18 is under active development with the goal of evolving into a fully autonomous, intelligent OSINT agent. Key upcoming developments are outlined in the project [Roadmap](docs/roadmap.md):

1. **Expanded Ingestion Sources:** Extend the ingestion pipeline beyond static files to live data streams – e.g. RSS feeds, social media APIs, and web scrapers. This will involve new modules or extensions to `src/ingest.py` while reusing the core pipeline steps (detect, parse, timestamp, hash, output, archive).
2. **Memory Braid Integration:** Develop the **Memory Braid** (long-term memory module) and integrate it with the drift detection engine. This includes logging **anchor vectors** over time and enhancing the Memory Ledger to support multi-layer recursive contexts, so the system maintains a stable knowledge base even as it grows.
3. **Summarization & Protector Enhancements:** Incorporate an LLM-driven summarizer that generates daily or real-time intelligence briefs from ingested data. All generated summaries will be passed through the Protector module for verification before archival or dissemination, ensuring outputs meet ethical and factual standards.
4. **Automation & Scheduling:** Implement automated scheduling and triggers (e.g., cron-like jobs or GitHub Actions scheduled workflows) to run the full pipeline on a regular basis. Additional tests will be written for new features to maintain high reliability, and CI/CD pipelines will enforce these checks.

These roadmap items reinforce Codex18’s goal of a **self-sufficient OSINT framework** that remains **ethically guided** and **contextually grounded**. Development will continue to uphold the founding motto and values, ensuring that as the system scales, *no context is lost and no principle is compromised*.

## Seal Workflow and GPG Signing

To preserve the integrity of the Codex18 development process, the repository employs a **“Seal” workflow** – an automated GitHub Actions routine that cryptographically signs each release cycle. This continuous integration workflow (defined in `.github/workflows/seal.yml`) runs on every push to the main branch (or version tags) and performs the following steps:

* **GPG Signature:** The workflow imports a GPG private key (stored securely in the repository secrets) and uses it to create an **empty commit** that serves as a cryptographic seal. The commit is GPG-signed with the trusted key and includes a message such as *“Seal commit: No Veteran Left Behind”*, embedding the project’s motto as a signature of authenticity.
* **Version Tagging:** It reads the project version (from a file like `VAULTIS.yml`) and tags the repository with a new version number corresponding to the sealed state. This provides a immutable reference point for each iteration of the intelligence framework.
* **Drift Analysis & Anchor Update:** After sealing, the workflow automatically runs the drift analysis engine to generate an updated truth vector report, then invokes the anchor rotation script to update the baseline if appropriate. By doing this at seal time, the repository’s memory baseline stays in sync with the latest ingested data, and any narrative drift is logged immediately in the commit history.
* **Ethical Backstop (Planned):** The workflow includes a placeholder for an **ethical constitution check** (using an external service codenamed *CarlAPI*). In future, this step will programmatically verify that the system’s state and outputs don’t violate ethical policies, adding an extra layer of accountability before finalizing the seal.

**Enabling the Seal Workflow:** To use the seal process in your own fork or deployment, you will need to configure a few secrets in the repository settings. Specifically, add your GPG private key as `GPG_PRIVATE_KEY` (ASCII-armored format) and set a `GPG_PASSPHRASE` that unlocks that key. For the official Nightwalker AI deployment, there is no passphrase set. Once these secrets are in place, the GitHub Actions runner will automatically sign and seal each commit to **maintain an auditable chain of trust**. If you prefer not to use this workflow, you can disable the GitHub Action, but the practice of GPG-signing releases is highly recommended for verifying the authenticity of updates.

The Seal workflow embodies Codex18’s focus on **operational integrity**. Every sealed commit effectively notarizes the state of the system – protecting the Memory Ledger’s continuity and signaling to collaborators and end-users that the update has passed all checks (tests, drift analysis, ethics review) and is cryptographically endorsed by the project maintainer.

## License

This project is released under the [MIT License](LICENSE). In short, you are free to use, modify, and distribute this software, provided that appropriate credit is given. See the [LICENSE](LICENSE) file for the full terms.

## Authorship and Credits

**Author:** Bryan A. Jewell (a.k.a. *Nightwalker Actual*) – creator and lead maintainer of the Codex series (ORCID iD: 0009-0001-2983-0505).

Portions of the design (memory ledger, agent architecture, etc.) draw from the developer’s ongoing research and personal journey, as documented in earlier Codex versions. All contributors are encouraged to uphold the project's guiding principles and ethos. The motto *“No Veteran Left Behind”* and the values it represents are carried forward in every aspect of Codex18’s evolution.

---

*Codex18 is an open-source intelligence framework built with an emphasis on clarity, integrity, and ethical AI operations. The documentation and repository structure are designed to ensure transparency and robustness, in alignment with Codex18’s ethical and symbolic foundations.*
No Veteran Left Behind. No Veteran Stands Alone.
