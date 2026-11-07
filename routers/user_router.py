from fastapi import APIRouter, Depends,  status, Request
from sqlalchemy.orm import Session

from database.session import get_session
from repositories.user_repository import UserRepository
from schemas.user import CreateUser
from services.user_service import UserService
from core.limiter import limiter


router = APIRouter(
        prefix="/users", tags=["users"], responses={404: {"description": "Not Found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minutes")
def create_user(request: Request,user: CreateUser, db: Session = Depends(get_session)):
        
        repository = UserRepository(db)
        service = UserService(repository)
        return service.create_user(user)


@router.get("/{user_id}")
@limiter.limit("10/minute")
def read_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_session)
):
    repository = UserRepository(db)
    service = UserService(repository)

    return service.get_user_by_id(user_id)