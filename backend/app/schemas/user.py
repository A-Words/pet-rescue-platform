from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    phone: str | None = None
    avatar_url: str | None = None


class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: str
    phone: str | None = None
    avatar_url: str | None = None
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
