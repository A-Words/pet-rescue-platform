from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class VisitReminder(Base):
    __tablename__ = "visit_reminders"

    reminder_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("adoption_applications.application_id"), nullable=False)
    adopter_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    adoptable_pet_id = Column(UUID(as_uuid=True), ForeignKey("adoptable_pets.adoptable_pet_id"), nullable=False)
    reminder_date = Column(Date, nullable=False)
    visit_date = Column(Date)
    status = Column(String(20), nullable=False, default="pending")
    visit_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    application = relationship("AdoptionApplication", back_populates="visit_reminders")
