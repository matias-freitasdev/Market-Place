import asyncio
from typing import List, Optional

from events import event_bus
from events.order_events import OrderCreatedEvent
from models.order import Order
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from schemas.order import OrderCreate, OrderRead


class OrderService:

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository | None = None):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def create_order(self, order_data: OrderCreate, buyer_id: int) -> OrderRead:
        return asyncio.run(self.create_order_async(order_data, buyer_id))

    async def create_order_async(self, order_data: OrderCreate, buyer_id: int) -> OrderRead:
        payload = order_data.model_dump()
        payload["buyer_id"] = buyer_id

        if self.product_repository is not None:
            product = self.product_repository.get_product_by_id(order_data.product_id)
            if product.stock < order_data.quantity:
                raise ValueError("Insufficient stock")

        order_entity = Order(**payload)

        try:
            created_order = self.order_repository.create_order(order_entity)

            if self.product_repository is not None:
                product = self.product_repository.get_product_by_id(order_data.product_id)
                new_stock = product.stock - order_data.quantity
                self.product_repository.update_stock(order_data.product_id, new_stock)

            await event_bus.publish_async(
                OrderCreatedEvent(
                    order_id=created_order.id,
                    buyer_id=created_order.buyer_id,
                    seller_id=created_order.seller_id,
                    product_name=created_order.name_product,
                    total=float(created_order.total),
                )
            )
            return OrderRead.model_validate(created_order, from_attributes=True)
        except Exception as e:
            raise ValueError("Failure to create order.") from e

    def get_order_by_id(self, order_id: int) -> Optional[OrderRead]:
        try:
            order = self.order_repository.get_order_by_id(order_id)
            return OrderRead.model_validate(order, from_attributes=True)
        except ValueError:
            return None

    async def get_order_by_id_async(self, order_id: int) -> Optional[OrderRead]:
        return self.get_order_by_id(order_id)

    def list_orders(self) -> List[OrderRead]:
        orders = self.order_repository.list_orders()
        return [OrderRead.model_validate(order, from_attributes=True) for order in orders]

    async def list_orders_async(self) -> List[OrderRead]:
        return self.list_orders()

    def order_by_user_id_seller(self, user_id: int) -> List[OrderRead]:
        orders = self.order_repository.order_by_user_id_seller(user_id)
        return [OrderRead.model_validate(order, from_attributes=True) for order in orders]

    async def order_by_user_id_seller_async(self, user_id: int) -> List[OrderRead]:
        return self.order_by_user_id_seller(user_id)

    def order_by_user_id_buyer(self, user_id: int) -> List[OrderRead]:
        orders = self.order_repository.order_by_user_id_buyer(user_id)
        return [OrderRead.model_validate(order, from_attributes=True) for order in orders]

    async def order_by_user_id_buyer_async(self, user_id: int) -> List[OrderRead]:
        return self.order_by_user_id_buyer(user_id)

