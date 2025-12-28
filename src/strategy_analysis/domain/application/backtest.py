from dataclasses import dataclass
from datetime import datetime

from market_data.ports.query import MarketDataQueryPort
from strategy_analysis.domain.strategy_spec import StrategySpec


@dataclass(frozen=True, slots=True)
class BacktestRequest:
    spec: StrategySpec
    start: datetime
    end: datetime


@dataclass(frozen=True, slots=True)
class BacktestResult:
    trades: int
    pnl: float


class BacktestService:
    def __init__(self, market_data: MarketDataQueryPort):
        self._market_data = market_data

    def run(self, req: BacktestRequest) -> BacktestResult:
        candles = self._market_data.get_candles(
            req.spec.instrument, req.spec.timeframe, req.start, req.end
        )
        # placeholder “strategy logic”
        trades = max(0, len(candles) // 100)
        pnl = float(trades) * 1.23
        return BacktestResult(trades=trades, pnl=pnl)
