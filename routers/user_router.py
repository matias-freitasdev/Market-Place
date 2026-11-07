from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from core.limiter import limiter
from database.session import get_session
from repositories.user_repository import UserRepository
from schemas.user import CreateUser
from services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minutes")
def create_user(request: Request, user: CreateUser, db: Session = Depends(get_session)):
    repository = UserRepository(db)
    service = UserService(repository)

    try:
        return service.create_user(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/{user_id}")
@limiter.limit("10/minute")
def read_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_session),
):
    repository = UserRepository(db)
    service = UserService(repository)

    try:
        return service.get_user_by_id(user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc