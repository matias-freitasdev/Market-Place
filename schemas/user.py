from pydantic import BaseModel, EmailStr, Field

class CreateUser(BaseModel):
    name: str = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=255)
    email: EmailStr = Field(min_length=6, max_length=100)

class loginUser(BaseModel):
    password: str = Field(min_length=8, max_length=255)
    email: EmailStr = Field(min_length=6, max_length=100)
