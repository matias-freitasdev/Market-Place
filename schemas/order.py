from decimal import Decimal

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    product_id: int
    name_product: str = Field(..., min_length=1, max_length=255)
    seller_id: int
    quantity: int = Field(..., gt=0)
    total: Decimal = Field(..., gt=0)
    status: str = "pending"


class OrderRead(BaseModel):
    id: int
    product_id: int
    name_product: str
    buyer_id: int
    seller_id: int
    quantity: int
    total: Decimal
    status: str

    model_config = {
        "from_attributes": True,
    }