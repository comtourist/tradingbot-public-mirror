# ADR-001: Store market data in ADLS Gen2 as Parquet

## Status
Accepted

## Context
We need cheap, scalable storage for historical market data that is friendly to Python/ML workflows.

## Decision
Use ADLS Gen2 as the system of record. Store curated datasets as Parquet partitioned by symbol/timeframe/date.

## Consequences
- Cheap storage and fast analytics
- Easy integration with Python and later distributed compute
- Requires consistent schema and partition strategy