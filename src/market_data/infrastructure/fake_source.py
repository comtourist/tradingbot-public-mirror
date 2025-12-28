from datetime import datetime, timedelta
from core.models import Candle, Instrument, Timeframe
from market_data.ports import MarketDataSourcePort


class FakeMarketDataSource(MarketDataSourcePort):
    def fetch_candles(
        self,
        instrument: Instrument,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
        candles: list[Candle] = []
        ts = start
        price = 100.0
        step = timedelta(minutes=1)

        while ts <= end:
            candles.append(
                Candle(
                    ts=ts,
                    open=price,
                    high=price + 1,
                    low=price - 1,
                    close=price + 0.5,
                    volume=None,
                )
            )
            ts += step
            price += 0.1

        return candles