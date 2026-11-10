from fastapi import Depends
from sqlalchemy.orm import Session

from database.session import get_session
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from services.order_service import OrderService


def get_order_service(db: Session = Depends(get_session)) -> OrderService:
    repository = OrderRepository(db)
    product_repository = ProductRepository(db)
    return OrderService(repository, product_repository)
