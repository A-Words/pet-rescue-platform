from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.schemas.user import UserResponse


class FoundClueCreate(BaseModel):
    description: str
    found_location: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    found_date: date
    contact_info: str
    photo_urls: list[str] | None = None


class FoundClueUpdate(BaseModel):
    status: str
    admin_notes: str | None = None


class FoundClueResponse(BaseModel):
    id: UUID
    lost_pet_id: UUID
    reporter_id: UUID
    photo_urls: list[str] | None = None
    description: str
    found_location: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    found_date: date
    contact_info: str
    status: str
    admin_notes: str | None = None
    reviewed_by: UUID | None = None
    reviewed_at: datetime | None = None
    created_at: datetime
    reporter: UserResponse | None = None

    model_config = {"from_attributes": True}
