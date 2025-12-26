# ADR-002: Ingestion Strategy (Daily Updates + Backfills)

## Status
Accepted

## Context
The platform must ingest historical and incremental market data to build and maintain a local “system of record” for analysis and (later) automated trading.

Key requirements:
- Support an initial single instrument (e.g., Nasdaq index) and later multiple instruments (e.g., Gold, Tesla, Treasuries)
- Efficiently ingest large historical datasets (backfill) and keep them updated daily
- Avoid over-complex orchestration early on
- Ensure idempotency (safe re-runs) and reproducibility
- Provide reliable state tracking (what was ingested, when, and with what result)
- Store data in a format optimized for Python/ML and scalable analytics

## Decision
We will implement a two-mode ingestion approach:

1. **Daily incremental ingestion** will run as an **Azure Function (Python)** on a timer trigger.
   - Purpose: fetch “new data since last successful ingestion” for each instrument/timeframe.
   - Writes vendor-native payloads to **ADLS Gen2 (raw zone)**.
   - Produces normalized Parquet datasets in **ADLS Gen2 (curated zone)**.
   - Updates ingestion progress in **Azure Database for PostgreSQL**.

2. **Historical backfill ingestion** will run as an **Azure Container Apps Job** (containerized batch job).
   - Purpose: ingest large historical date ranges and/or many instruments.
   - Runs on demand (manual trigger in early phases; queue-driven later).
   - Writes raw and curated outputs to ADLS Gen2.
   - Updates ingestion progress in PostgreSQL.

The data lake (ADLS Gen2) is the **system of record**, while PostgreSQL stores **metadata and ingestion state**.

## Data flow and storage conventions
### Raw zone (immutable)
- Store provider responses as-is (JSON/CSV/NDJSON) for traceability and reproducibility.
- Raw data is append-only; never edited in place.
- Example path pattern:
  - `raw/vendor=<vendor>/dataset=bars/timeframe=<tf>/symbol=<sym>/year=<YYYY>/month=<MM>/...`

### Curated zone (normalized Parquet)
- Store cleaned, deduplicated, schema-enforced datasets in Parquet.
- Partition by symbol, timeframe, and date components for efficient reads.
- Example path pattern:
  - `curated/dataset=bars/timeframe=<tf>/symbol=<sym>/year=<YYYY>/month=<MM>/part-*.parquet`

### Canonical bars schema (minimum)
Curated bars datasets will conform to a consistent schema across instruments:
- `ts` (UTC timestamp)
- `open`, `high`, `low`, `close` (numeric)
- `volume` (numeric, nullable if not applicable)
- `symbol` (string)
- `timeframe` (string, e.g. `1d`)
- `source` (string)

## Ingestion state tracking
PostgreSQL will store ingestion state for each instrument/timeframe, at minimum:
- `instrument_id`
- `timeframe`
- `last_ts` (last successfully ingested timestamp)
- `status` (e.g., `success`, `failed`, `partial`)
- `updated_at`
- `message` (error or diagnostic text)

This enables:
- Incremental ingestion (“continue from last_ts”)
- Monitoring and troubleshooting
- Safe reprocessing

## Idempotency and correctness rules
- Ingestion must be **idempotent**: re-running a job for the same date range must not create duplicates.
- Curated writes must be deterministic: same inputs → same outputs.
- Deduplication is applied at curated layer using primary keys such as:
  - `(symbol, timeframe, ts)`
- Timestamps are normalized to **UTC** before writing curated outputs.

## Consequences
### Positive
- Simple and cost-effective for early-stage development
- Scales naturally: backfills can be parallelized later without changing fundamentals
- Clear separation between raw provenance and curated analytical datasets
- Supports Python/ML workflows efficiently via Parquet + partitioning
- PostgreSQL provides lightweight, reliable operational state tracking

### Negative / Trade-offs
- Two execution environments (Functions + container jobs) require consistent shared code packaging
- Requires clear schema governance and partitioning conventions early
- Very high-frequency data (tick/minute) may require future optimization (e.g., dedicated time-series store or ADX)

## Future evolution
- Add **Azure Storage Queue** to enqueue ingestion tasks and drive parallel workers (Phase 2).
- Add “hot cache” tables in PostgreSQL for recent data used by strategies.
- Introduce corporate actions handling for equities (splits/dividends) when needed.
- Consider Azure Data Explorer (ADX) only if query patterns or data frequency outgrow Postgres + Parquet.