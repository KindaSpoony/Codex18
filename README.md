# Codex18 Repository

Codex18 is the next evolution of our data analysis platform, incorporating automated data ingestion and processing for Founder's Reports. It builds on lessons learned in Codex17 and introduces a robust ingestion pipeline to streamline report analysis.

## Ingestion Pipeline for Founder's Reports

**Status: Live and Operational** – The Codex18 system now includes an automated ingestion module that is actively monitoring and processing Founder's Reports. Any new report placed into the `data/reports_incoming` directory will be automatically ingested by the system:

- **Metadata Extraction**: Each report is expected to contain YAML front matter at the top of the file. The ingestion module parses this front matter to extract structured metadata (e.g. title, author, date, and other report attributes).  
- **Secure Timestamping**: When a report is ingested, the system attaches a current UTC timestamp to the record to log when it was processed. This timestamp is generated in a time-zone safe manner (UTC) to ensure consistency across systems.  
- **Content Hashing**: The body of the report (excluding the front matter) is hashed using SHA-256. This produces a unique fingerprint for the content, which can be used for integrity verification or to detect duplicate reports.  
- **JSON Record Creation**: A structured JSON record is created for each report and saved to `data/analysis_output`. This JSON includes the extracted metadata, the ingestion timestamp, the SHA-256 hash, and the full text content of the report. The structured format facilitates downstream analysis and querying of the reports.  
- **Archival of Originals**: After successful processing, the original report file is moved to `data/chronicle/archive`. Archiving ensures the original content is preserved for compliance and historical reference, while keeping the incoming directory clean. The system will append a timestamp to the filename upon archiving if a file with the same name already exists in the archive, preventing any filename collisions.  

With this pipeline in place, Codex18 can reliably transform incoming Founder's Reports into structured data for analysis, all while maintaining an audit trail of original documents and processing times.

## Repository Structure
codex18/
├── data/
│   ├── reports_incoming/ # directory for incoming Founder's Report files (raw format)
│   ├── analysis_output/  # directory where processed JSON records are stored
│   └── chronicle/
│       └── archive/      # archive for original reports after ingestion
├── ingest.py             # ingestion pipeline script for Founder's Reports (automated processing)
├── ...                   # other project modules and files
└── README.md             # project documentation (this file)
 
*(Remaining sections of the README omitted for brevity; they include setup instructions, usage examples, and contributor guidelines, which remain unchanged.)*
