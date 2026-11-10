from __future__ import annotations

from events.event_bus import event_bus
from events.order_events import OrderCreatedEvent


async def send_buyer_purchase_notification(event: OrderCreatedEvent) -> dict:
    return {
        "recipient": "buyer",
        "user_id": event.buyer_id,
        "order_id": event.order_id,
        "message": (
            f"Pedido {event.order_id} confirmado com sucesso. "
            f"Você comprou {event.product_name} pelo valor de R$ {event.total:.2f}."
        ),
    }


async def send_seller_sale_notification(event: OrderCreatedEvent) -> dict:
    return {
        "recipient": "seller",
        "user_id": event.seller_id,
        "order_id": event.order_id,
        "message": (
            f"Venda realizada: pedido {event.order_id} para {event.product_name}. "
            f"Recebimento estimado de R$ {event.total:.2f}."
        ),
    }


def register_handlers() -> None:
    if getattr(event_bus, "_handlers_registered", False):
        return

    event_bus.subscribe(OrderCreatedEvent, send_buyer_purchase_notification)
    event_bus.subscribe(OrderCreatedEvent, send_seller_sale_notification)
    event_bus._handlers_registered = True
