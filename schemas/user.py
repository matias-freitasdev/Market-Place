from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=255)
    email: EmailStr = Field(min_length=6, max_length=100)


class loginUser(BaseModel):
    password: str = Field(min_length=8, max_length=255)
    email: EmailStr = Field(min_length=6, max_length=100)


class UserRead(BaseModel):
    username: str

