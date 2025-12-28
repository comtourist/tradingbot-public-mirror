from __future__ import annotations

from datetime import datetime

from src.core.models import Candle, Instrument, Timeframe
from src.market_data.infrastructure.memory_store import InMemoryMarketDataStore


def test_store_query_filters_by_time_range() -> None:
    store = InMemoryMarketDataStore()
    instrument = Instrument("EURUSD")
    timeframe = Timeframe("M1")

    candles = [
        Candle(ts=datetime(2025, 1, 1, 0, 0, 0), open=1, high=1, low=1, close=1),
        Candle(ts=datetime(2025, 1, 1, 0, 1, 0), open=1, high=1, low=1, close=1),
        Candle(ts=datetime(2025, 1, 1, 0, 2, 0), open=1, high=1, low=1, close=1),
    ]

    store.write_candles(instrument, timeframe, candles)

    result = store.get_candles(
        instrument,
        timeframe,
        datetime(2025, 1, 1, 0, 1, 0),
        datetime(2025, 1, 1, 0, 2, 0),
    )

    assert [c.ts for c in result] == [
        datetime(2025, 1, 1, 0, 1, 0),
        datetime(2025, 1, 1, 0, 2, 0),
    ]
