from market_data.infrastructure.fake_source import FakeMarketDataSource
from market_data.infrastructure.memory_store import InMemoryMarketDataStore
from market_data.ingestion.ingest_market_data import IngestMarketDataService
from strategy_analysis.domain.application.backtest import BacktestService


def build_services() -> tuple[IngestMarketDataService, BacktestService]:
    store = InMemoryMarketDataStore()
    source = FakeMarketDataSource()

    ingest = IngestMarketDataService(source=source, store=store)
    backtest = BacktestService(market_data=store)

    return ingest, backtest