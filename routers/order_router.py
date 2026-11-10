from typing import List

from fastapi import APIRouter, Depends, Request, status

from core.limiter import limiter
from dependencies.order_deps import get_order_service
from dependencies.product_deps import get_current_active_user
from models.user import User
from schemas.order import OrderCreate, OrderRead
from services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderRead)
@limiter.limit("5/minutes")
async def create_order(
    request: Request,
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.create_order_async(order_data, buyer_id=current_user.id)


@router.get("/my-orders", response_model=List[OrderRead])
@limiter.limit("5/minutes")
async def list_orders_by_buyer(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.order_by_user_id_buyer_async(current_user.id)


@router.get("/seller/{seller_id}", response_model=List[OrderRead])
@limiter.limit("5/minutes")
async def list_orders_by_seller(
    request: Request,
    seller_id: int,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.order_by_user_id_seller_async(seller_id)


@router.get("/{order_id}", response_model=OrderRead)
@limiter.limit("5/minutes")
async def get_order_by_id(
    request: Request,
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.get_order_by_id_async(order_id)