from typing import Protocol
from core.models import Candle, Instrument, Timeframe


class MarketDataStorePort(Protocol):
    def write_candles(
        self,
        instrument: Instrument,
        timeframe: Timeframe,
        candles: list[Candle],
    ) -> None:
        ...