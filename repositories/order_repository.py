from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.order import Order


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_order(self, order: Order) -> Order:
        try:
            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)
            return order
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError("Failure to create order in the database.") from e

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        statement = select(Order).where(Order.id == order_id)
        order = self.session.scalar(statement)

        if not order:
            raise ValueError("Order not found")

        return order

    def list_orders(self) -> List[Order]:
        statement = select(Order)
        return self.session.scalars(statement).all()

    def order_by_user_id_seller(self, user_id: int) -> List[Order]:
        statement = select(Order).where(Order.seller_id == user_id)
        return self.session.scalars(statement).all()

    def order_by_user_id_buyer(self, user_id: int) -> List[Order]:
        statement = select(Order).where(Order.buyer_id == user_id)
        return self.session.scalars(statement).all()