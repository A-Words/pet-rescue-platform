from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.adoptable_pet import AdoptablePetResponse
from app.schemas.review_record import ReviewRecordResponse


class AdoptionApplicationCreate(BaseModel):
    adoptable_pet_id: UUID
    applicant_name: str
    applicant_phone: str
    applicant_address: str
    applicant_id_number: str
    housing_type: str | None = None
    has_other_pets: bool = False
    adoption_reason: str
    experience_description: str | None = None


class AdoptionApplicationResponse(BaseModel):
    application_id: UUID
    adoptable_pet_id: UUID
    applicant_id: UUID
    applicant_name: str
    applicant_phone: str
    applicant_address: str
    applicant_id_number: str
    housing_type: str | None = None
    has_other_pets: bool
    adoption_reason: str
    experience_description: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime
    pet: AdoptablePetResponse | None = None
    review_records: list[ReviewRecordResponse] | None = None

    model_config = {"from_attributes": True}


class ApplicationReview(BaseModel):
    decision: str
    review_notes: str | None = None
