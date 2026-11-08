from typing import Optional

from models.user import User
from core.security import hash_password, verify_password, create_access_token
from repositories.user_repository import UserRepository
from schemas.user import CreateUser, loginUser, UserRead


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: CreateUser) -> UserRead:
        try:
            existing_user = self.user_repository.get_by_email(user.email)
        except ValueError:
            existing_user = None

        if existing_user:
            raise ValueError("Email already registered")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
        )
        return self.user_repository.create(new_user)

    def authenticate_user(self, user: loginUser):
        try:
            existing_user = self.user_repository.get_by_email(user.email)
        except ValueError:
            existing_user = None

        if not existing_user or not verify_password(user.password, existing_user.password):
            raise ValueError("Email or Password Is Incorret")

        access_token = create_access_token(user.email)
        return {"access_token": access_token, "token_typer": "bearer"}

    def list_users(self):
        try:
            return self.user_repository.get_all()
        except ValueError as exc:
            raise ValueError("No users registered yet") from exc

    def get_user_by_id(self, id: int) -> Optional[UserRead]:
        try:
            return self.user_repository.get_by_id(id)
        except ValueError as exc:
            raise ValueError("User not found") from exc

    def delete_user(self, id: int):
        return self.user_repository.delete_user(id)
