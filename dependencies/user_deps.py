from fastapi import Depends
from sqlalchemy.orm import Session
from database.session import get_session
from repositories.user_repository import UserRepository
from services.user_service import UserService

def get_user_service(db: Session = Depends(get_session)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)