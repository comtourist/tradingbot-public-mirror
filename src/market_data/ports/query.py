from typing import Protocol
from datetime import datetime
from core.models import Candle, Instrument, Timeframe


class MarketDataQueryPort(Protocol):
    def get_candles(
        self,
        instrument: Instrument,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
        ...