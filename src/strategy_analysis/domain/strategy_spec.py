from dataclasses import dataclass
from core.models import Instrument, Timeframe


@dataclass(frozen=True, slots=True)
class StrategySpec:
    name: str
    instrument: Instrument
    timeframe: Timeframe
    # later: parameters, entry/exit rules, risk rules, etc.
