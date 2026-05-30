from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReviewRecordResponse(BaseModel):
    id: UUID
    application_id: UUID
    reviewer_id: UUID
    decision: str
    review_notes: str | None = None
    reviewed_at: datetime

    model_config = {"from_attributes": True}
