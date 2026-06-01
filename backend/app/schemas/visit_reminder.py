from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class VisitReminderResponse(BaseModel):
    reminder_id: UUID
    application_id: UUID
    adopter_id: UUID
    adoptable_pet_id: UUID
    reminder_date: date
    visit_date: date | None = None
    status: str
    visit_notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class VisitReminderUpdate(BaseModel):
    status: str | None = None
    visit_date: date | None = None
    visit_notes: str | None = None
