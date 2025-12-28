from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Candle:
    """
    Normalized OHLCV candle used across the entire platform.
    """

    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None

    def is_bullish(self) -> bool:
        return self.close > self.open

    def is_bearish(self) -> bool:
        return self.close < self.open
