from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.schemas.user import UserResponse


class LostPetCreate(BaseModel):
    pet_name: str
    pet_type: str
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age_description: str | None = None
    photo_urls: list[str] | None = None
    description: str
    lost_date: date
    lost_location: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    contact_info: str
    reward_amount: Decimal | None = None


class LostPetUpdate(BaseModel):
    pet_name: str | None = None
    pet_type: str | None = None
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age_description: str | None = None
    photo_urls: list[str] | None = None
    description: str | None = None
    lost_date: date | None = None
    lost_location: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    contact_info: str | None = None
    reward_amount: Decimal | None = None


class LostPetResponse(BaseModel):
    id: UUID
    user_id: UUID
    pet_name: str
    pet_type: str
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age_description: str | None = None
    photo_urls: list[str] | None = None
    description: str
    lost_date: date
    lost_location: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    contact_info: str
    reward_amount: Decimal | None = None
    status: str
    created_at: datetime
    updated_at: datetime
    user: UserResponse | None = None

    model_config = {"from_attributes": True}


class LostPetListParams(BaseModel):
    page: int = 1
    page_size: int = 12
    pet_type: str | None = None
    status: str | None = None
    keyword: str | None = None
