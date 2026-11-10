from typing import Optional

from models.order import Order
from repositories.order_repository import OrderRepository
from schemas.order import OrderCreate, OrderRead


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, order_data: OrderCreate) -> OrderRead:
        payload = order_data.model_dump()
        order_entity = Order(**payload)

        try:
            created_order = self.order_repository.create_order(order_entity)
            return OrderRead.model_validate(created_order, from_attributes=True)
        except Exception as e:
            raise ValueError("Failure to create order in the database.") from e

    def get_order_by_id(self, order_id: int) -> Optional[OrderRead]:
        try:
            order = self.order_repository.get_order_by_id(order_id)
            return OrderRead.model_validate(order, from_attributes=True)
        except ValueError:
            return None
