from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


class DomainEvent:
    def __init__(self) -> None:
        self.event_id = uuid4().hex
        self.occurred_at = datetime.now(timezone.utc)
