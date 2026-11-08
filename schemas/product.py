from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    product_name: str
    price: float
    stock: int
    category: str


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    price: float
    stock: int
    category: str
    user_id: int


class DeleteProduct(BaseModel):
    id: int
