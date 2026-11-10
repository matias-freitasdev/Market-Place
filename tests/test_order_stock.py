from decimal import Decimal

import pytest

from schemas.order import OrderCreate
from services.order_service import OrderService


class FakeProductRepository:
    def __init__(self, product):
        self.product = product

    def get_product_by_id(self, product_id):
        return self.product

    def update_stock(self, product_id, new_stock):
        self.product.stock = new_stock
        return self.product


class FakeOrderRepository:
    def __init__(self):
        self.saved_order = None

    def create_order(self, order):
        order.id = 10
        self.saved_order = order
        return order


def build_product(stock):
    return type(
        "ProductStub",
        (),
        {"id": 5, "product_name": "Notebook", "stock": stock, "price": 100.0, "seller_id": 9},
    )()


def test_order_reduces_stock_when_purchased():
    product = build_product(3)
    service = OrderService(FakeOrderRepository(), FakeProductRepository(product))
    payload = OrderCreate(
        product_id=5,
        name_product="Notebook",
        seller_id=9,
        quantity=3,
        total=Decimal("300.00"),
        status="pending",
    )

    result = service.create_order(payload, buyer_id=7)

    assert result.quantity == 3
    assert product.stock == 0


def test_order_fails_when_stock_insufficient():
    product = build_product(2)
    service = OrderService(FakeOrderRepository(), FakeProductRepository(product))
    payload = OrderCreate(
        product_id=5,
        name_product="Notebook",
        seller_id=9,
        quantity=3,
        total=Decimal("300.00"),
        status="pending",
    )

    with pytest.raises(ValueError, match="Insufficient stock"):
        service.create_order(payload, buyer_id=7)
