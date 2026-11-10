from __future__ import annotations

import asyncio
import inspect
from collections import defaultdict
from typing import Any, Callable

from events.base_event import DomainEvent


class EventBus:
    def __init__(self):
        self._handlers: dict[type[DomainEvent], list[Callable[[DomainEvent], Any]]] = defaultdict(list)
        self._handlers_registered = False

    def subscribe(self, event_type: type[DomainEvent], handler: Callable[[DomainEvent], Any]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> list[Any]:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.publish_async(event))

        return self._publish_sync(event)

    async def publish_async(self, event: DomainEvent) -> list[Any]:
        results: list[Any] = []

        for event_type, handlers in self._handlers.items():
            if isinstance(event, event_type):
                for handler in handlers:
                    result = handler(event)
                    if inspect.isawaitable(result):
                        result = await result
                    results.append(result)

        return results

    def _publish_sync(self, event: DomainEvent) -> list[Any]:
        results: list[Any] = []

        for event_type, handlers in self._handlers.items():
            if isinstance(event, event_type):
                for handler in handlers:
                    result = handler(event)
                    if inspect.isawaitable(result):
                        raise RuntimeError(
                            "Async handlers cannot be published from a synchronous context. "
                            "Use await event_bus.publish_async(event)."
                        )
                    results.append(result)

        return results


event_bus = EventBus()
