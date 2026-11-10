from events import event_bus
from events.order_events import OrderCreatedEvent
from services.order_service import OrderService


class FakeRepository:
    def __init__(self):
        self.saved_order = None

    def create_order(self, order):
        order.id = 42
        self.saved_order = order
        return order

    def get_order_by_id(self, order_id):
        return None

    def list_orders(self):
        return []

    def order_by_user_id_seller(self, user_id):
        return []

    def order_by_user_id_buyer(self, user_id):
        return []


def test_order_created_event_emits_notifications():
    events = []

    def capture(event):
        events.append(event)

    event_bus.subscribe(OrderCreatedEvent, capture)

    service = OrderService(FakeRepository())
    created = service.create_order(
        type(
            "Payload",
            (),
            {
                "model_dump": lambda self: {
                    "product_id": 3,
                    "name_product": "Notebook",
                    "seller_id": 9,
                    "quantity": 1,
                    "total": 3999.99,
                    "status": "pending",
                }
            },
        )(),
        buyer_id=7,
    )

    assert created.buyer_id == 7
    assert len(events) >= 1
    assert events[0].seller_id == 9
    assert events[0].buyer_id == 7
    assert events[0].product_name == "Notebook"
