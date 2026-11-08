from fastapi import Depends
from sqlalchemy.orm import Session
from database.session import get_session
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from core.security import get_current_user
from services.product_service import ProductService

# 1. Injeta o Service de Produtos automaticamente
def get_product_service(db: Session = Depends(get_session)) -> ProductService:
    repository = ProductRepository(db)
    return ProductService(repository)

# 2. Injeta o Usuário Logado automaticamente (buscando do banco pelo token)
def get_current_active_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    user_repository = UserRepository(db)
    user = user_repository.get_by_email(current_user["sub"])
    if not user:
        raise ValueError("User not found")
    return user