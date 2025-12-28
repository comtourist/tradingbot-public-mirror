from dataclasses import dataclass
from datetime import datetime
from core.models import Instrument, Timeframe

from market_data.ports.source import MarketDataSourcePort
from market_data.ports.store import MarketDataStorePort


@dataclass(frozen=True, slots=True)
class IngestRequest:
    instrument: Instrument
    timeframe: Timeframe
    start: datetime
    end: datetime


class IngestMarketDataService:
    def __init__(self, source: MarketDataSourcePort, store: MarketDataStorePort):
        self._source = source
        self._store = store

    def run(self, req: IngestRequest) -> int:
        candles = self._source.fetch_candles(req.instrument, req.timeframe, req.start, req.end)
        self._store.write_candles(req.instrument, req.timeframe, candles)
        return len(candles)
