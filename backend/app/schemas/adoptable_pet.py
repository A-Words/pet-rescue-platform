from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class AdoptablePetCreate(BaseModel):
    pet_name: str
    pet_type: str
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age_months: int | None = None
    photo_urls: list[str] | None = None
    description: str | None = None
    health_status: str = "healthy"
    is_vaccinated: bool = False
    is_dewormed: bool = False
    is_sterilized: bool = False
    rescue_station: str | None = None
    intake_date: date


class AdoptablePetUpdate(BaseModel):
    pet_name: str | None = None
    pet_type: str | None = None
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age_months: int | None = None
    photo_urls: list[str] | None = None
    description: str | None = None
    health_status: str | None = None
    is_vaccinated: bool | None = None
    is_dewormed: bool | None = None
    is_sterilized: bool | None = None
    rescue_station: str | None = None
    intake_date: date | None = None


class AdoptablePetResponse(BaseModel):
    id: UUID
    pet_name: str
    pet_type: str
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age_months: int | None = None
    photo_urls: list[str] | None = None
    description: str | None = None
    health_status: str
    is_vaccinated: bool
    is_dewormed: bool
    is_sterilized: bool
    adoption_status: str
    rescue_station: str | None = None
    intake_date: date
    created_at: datetime
    updated_at: datetime
    application_count: int | None = None

    model_config = {"from_attributes": True}
