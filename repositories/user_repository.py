from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        user = self.session.scalar(statement)
        if not user:
            raise ValueError("User not found")
        return user

    def get_by_id(self, id: int):
        statement = select(User).where(User.id == id)
        user = self.session.scalar(statement)
        if not user:
            raise ValueError("User not found")
        return user

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all(self):
        statement = select(User)
        users = self.session.scalars(statement).all()
        if not users:
            raise ValueError("No users registered yet")
        return users

    def delete_user(self, user_id: int):
        statement = select(User).where(User.id == user_id)

        user = self.session.scalar(statement)

        if not user:
            raise ValueError("User not found")

        self.session.delete(user)
        self.session.commit()

        return True