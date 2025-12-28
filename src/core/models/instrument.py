from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Instrument:
    """
    A tradable instrument, independent of venue or broker implementation.
    """

    symbol: str  # e.g. "EURUSD", "AAPL", "BTCUSD"
    venue: str | None = None  # optional, e.g. "CAPITALCOM"

    def __str__(self) -> str:
        return self.symbol if self.venue is None else f"{self.symbol}@{self.venue}"
