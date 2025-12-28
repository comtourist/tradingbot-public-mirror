from enum import Enum


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class StrategyState(str, Enum):
    DRAFT = "DRAFT"
    BACKTESTED = "BACKTESTED"
    LIVE = "LIVE"
    PAUSED = "PAUSED"
    RETIRED = "RETIRED"
