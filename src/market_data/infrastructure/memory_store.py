from collections import defaultdict
from datetime import datetime
from core.models import Candle, Instrument, Timeframe
from market_data.ports import MarketDataQueryPort, MarketDataStorePort


class InMemoryMarketDataStore(MarketDataStorePort, MarketDataQueryPort):
    def __init__(self) -> None:
        self._data: dict[tuple[str, str], list[Candle]] = defaultdict(list)

    def write_candles(
        self,
        instrument: Instrument,
        timeframe: Timeframe,
        candles: list[Candle],
    ) -> None:
        key = (instrument.symbol, timeframe.name)
        self._data[key].extend(candles)
        self._data[key].sort(key=lambda c: c.ts)

    def get_candles(
        self,
        instrument: Instrument,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
        key = (instrument.symbol, timeframe.name)
        return [c for c in self._data.get(key, []) if start <= c.ts <= end]