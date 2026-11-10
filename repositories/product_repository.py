from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.product import Product

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_product_by_id(self, product_id: int) -> Product:
        statement = select(Product).where(Product.id == product_id)
        product = self.session.scalar(statement)

        if not product:
            raise ValueError("Product not found")
            
        return product

    def list_products_by_user(self, user_id: int) -> List[Product]:
        statement = select(Product).where(Product.user_id == user_id)
        user_products = self.session.scalars(statement).all()
        
        # Opcional: retornar lista vazia é o comportamento padrão para listagens
        return user_products

    def search_products_by_name(self, product_name: str) -> List[Product]:
        statement = select(Product).where(Product.product_name == product_name)
        products = self.session.scalars(statement).all()
        
        if not products:
            raise ValueError("No products found with this name")

        return products

    def create_product(self, product: Product) -> Product:
        try:
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return product
        except SQLAlchemyError as e:
            self.session.rollback()
            
            raise ValueError("Failure to save the product in the database.") from e

    def update_stock(self, product_id: int, new_stock: int) -> Product:
        product = self.get_product_by_id(product_id)
        product.stock = new_stock

        try:
            self.session.commit()
            self.session.refresh(product)
            return product
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError("Failure to update product stock.") from e

    def delete_product(self, product_id: int, user_id: int) -> dict:
        statement = select(Product).where(
            Product.id == product_id,
            Product.user_id == user_id
        )
        product = self.session.scalar(statement)

        if not product:
            raise ValueError("Product not found or not owned by this user")

        try:
            self.session.delete(product)
            self.session.commit()
            return {"msg": f"Product {product.id} deleted successfully"}
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError("Failure to delete the product in the database.") from e

    def update_product(self,
    product_id: int,
    update_data: dict,
    user_id: int
) -> Product:

        statement = select(Product).where(
        Product.id == product_id,
        Product.user_id == user_id
        )

        product = self.session.scalar(statement)

        if not product:
            raise ValueError("Product not found or not owned by this user")

        try:
            for key, value in update_data.items():
                if hasattr(product, key) and value is not None:
                    setattr(product, key, value)

            self.session.commit()
            self.session.refresh(product)

            return product

        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError("Failure to update product") from e