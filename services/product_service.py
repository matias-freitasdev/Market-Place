from typing import Optional

from models.product import Product
from repositories.product_repository import ProductRepository
from schemas.product import ProductCreate, ProductRead


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository


    def create_product(self, product_data: ProductCreate, user_id: int) -> ProductRead:
        payload = product_data.model_dump()
        payload["user_id"] = user_id
        product_entity = Product(**payload)

        try:
            created_product = self.product_repository.create_product(product_entity)
            return ProductRead.model_validate(created_product, from_attributes=True)
        except Exception as e:
            raise ValueError("Failure to create product in the database.") from e


    def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        try:
            product = self.product_repository.get_product_by_id(product_id)
            return ProductRead.model_validate(product, from_attributes=True)
        except ValueError:
            return None


    def list_products_by_user(self, user_id: int) -> list[ProductRead]:
        products = self.product_repository.list_products_by_user(user_id)
        return [ProductRead.model_validate(product, from_attributes=True) for product in products]


    def search_products_by_name(self, product_name: str) -> list[ProductRead]:
        products = self.product_repository.search_products_by_name(product_name)
        return [ProductRead.model_validate(product, from_attributes=True) for product in products]


    def delete_product(self, product_id: int, user_id: int):
        return self.product_repository.delete_product(product_id, user_id)


    def update_product(
    self,
    product_id: int,
    update_data: dict,
    user_id: int
) -> ProductRead:
        
        product = self.product_repository.update_product(
        product_id,
        update_data,
        user_id
    )

        return ProductRead.model_validate(
        product,
        from_attributes=True
        )