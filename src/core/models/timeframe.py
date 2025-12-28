from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Timeframe:
    """
    Represents the aggregation period of market data.
    """

    name: str  # e.g. "M1", "M5", "H1", "D1"

    def __str__(self) -> str:
        return self.name
