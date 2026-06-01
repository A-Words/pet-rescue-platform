from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ReviewRecord(Base):
    __tablename__ = "review_records"

    review_record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("adoption_applications.application_id"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    decision = Column(String(20), nullable=False)
    review_notes = Column(Text)
    reviewed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    application = relationship("AdoptionApplication", back_populates="review_records")
