from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from events.base_event import DomainEvent


@dataclass(slots=True, kw_only=True)
class OrderCreatedEvent(DomainEvent):
    order_id: int
    buyer_id: int
    seller_id: int
    product_name: str
    total: float
    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
