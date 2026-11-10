from fastapi import APIRouter, Depends, Request, status

from core.limiter import limiter
from schemas.user import CreateUser, UserRead, loginUser, DeletUser
from services.user_service import UserService
from dependencies.user_deps import get_user_service
from core.security import create_access_token,create_refresh_token,verify_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
@limiter.limit("5/minutes")
def create_user(
    request: Request, 
    user: CreateUser, 
    service: UserService = Depends(get_user_service)
):
    
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserRead)
@limiter.limit("10/minute")
def read_user(
    request: Request,
    user_id: int,
    service: UserService = Depends(get_user_service),
):

    return service.get_user_by_id(user_id)

@router.post("/auth-login")
@limiter.limit("5/minutes")
def login_user(
    request: Request,
    user: loginUser,
    service: UserService = Depends(get_user_service)
):
    return service.authenticate_user(user)

@router.get("list-all-users")
@limiter.limit("5/minutes")
async def lits_users(
    request: Request,
    service: UserService = Depends(get_user_service)
):
    return service.list_users()

@router.delete("delete-user")
@limiter.limit("5/minutes")
def delete_user(
    request: Request,
    user_id: DeletUser,
    service: UserService = Depends(get_user_service)
):
    return service.delete_user(user_id)