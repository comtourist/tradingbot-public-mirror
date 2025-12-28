from __future__ import annotations

from dataclasses import dataclass
from core.models import Instrument
from typing import Protocol


@dataclass(frozen=True, slots=True)
class OrderIntent:
    instrument: Instrument
    side: str  # "BUY"/"SELL" (later enum)
    quantity: float


@dataclass(frozen=True, slots=True)
class OrderAck:
    order_id: str
    status: str


class BrokerPort(Protocol):
    def place_order(self, intent: OrderIntent) -> OrderAck: ...
