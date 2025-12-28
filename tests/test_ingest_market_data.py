from __future__ import annotations

from datetime import datetime

from src.market_data.infrastructure.fake_source import FakeMarketDataSource
from src.market_data.infrastructure.memory_store import InMemoryMarketDataStore
from src.market_data.ingestion.ingest_market_data import IngestMarketDataService, IngestRequest
from src.core.models import Instrument, Timeframe


def test_ingest_market_data_writes_to_store_and_returns_count() -> None:
    source = FakeMarketDataSource()
    store = InMemoryMarketDataStore()
    svc = IngestMarketDataService(source=source, store=store)

    req = IngestRequest(
        instrument=Instrument("EURUSD"),
        timeframe=Timeframe("M1"),
        start=datetime(2025, 1, 1, 0, 0, 0),
        end=datetime(2025, 1, 1, 0, 4, 0),
    )

    written = svc.run(req)
    assert written > 0

    candles = store.get_candles(req.instrument, req.timeframe, req.start, req.end)
    assert len(candles) == written
    assert candles == sorted(candles, key=lambda c: c.ts)
    assert candles[0].ts >= req.start
    assert candles[-1].ts <= req.end


def test_ingest_market_data_second_run_currently_duplicates_in_memory_store() -> None:
    """
    This documents current placeholder behavior.

    When you implement deduplication in the store, change this to assert
    that the candle count stays the same after re-ingesting the same range.
    """
    source = FakeMarketDataSource()
    store = InMemoryMarketDataStore()
    svc = IngestMarketDataService(source=source, store=store)

    req = IngestRequest(
        instrument=Instrument("EURUSD"),
        timeframe=Timeframe("M1"),
        start=datetime(2025, 1, 1, 0, 0, 0),
        end=datetime(2025, 1, 1, 0, 2, 0),
    )

    first = svc.run(req)
    second = svc.run(req)

    candles = store.get_candles(req.instrument, req.timeframe, req.start, req.end)
    assert len(candles) == first + second
