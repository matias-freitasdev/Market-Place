from typing import List
from fastapi import APIRouter, Depends, Request, status

from core.limiter import limiter
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from services.product_service import ProductService
from dependencies.product_deps import get_product_service, get_current_active_user  
from models.user import User

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductRead)
@limiter.limit("5/minutes")
def create_product(
    request: Request,
    product: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    service: ProductService = Depends(get_product_service),
):

    return service.create_product(product, user_id=current_user.id)


@router.get("/{product_id}", response_model=ProductRead)
@limiter.limit("5/minutes")
def get_product_by_id(
    request: Request,
    product_id: int,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    return service.get_user_by_id(product_id)


@router.get("/my-products", response_model=List[ProductRead])
@limiter.limit("5/minutes")
def list_products_by_user(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    service: ProductService = Depends(get_product_service)
):
    return service.get_user_products(current_user.id)


@router.get("/search/{product_name}", response_model=List[ProductRead])
@limiter.limit("10/minutes")
def search_products_by_name(
    request: Request,
    product_name: str,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_active_user)
):
    return service.search_products_by_name(product_name)


@router.delete("/{product_id}")
@limiter.limit("10/minutes")
def delete_product(
    request: Request,
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    service: ProductService = Depends(get_product_service),
):
    return service.delete_product(product_id, current_user.id)


@router.patch("/{product_id}", response_model=ProductRead)
@limiter.limit("10/minutes")
def update_product(
    request: Request,
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_active_user),
    service: ProductService = Depends(get_product_service),
):
    return service.update_product(
        product_id=product_id,
        update_data=product_data.model_dump(exclude_unset=True),
        user_id=current_user.id
    )