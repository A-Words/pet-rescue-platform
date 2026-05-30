from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class AdoptionApplication(Base):
    __tablename__ = "adoption_applications"
    __table_args__ = (UniqueConstraint("pet_id", "applicant_id", name="uq_pet_applicant"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("adoptable_pets.id"), nullable=False)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    applicant_name = Column(String(50), nullable=False)
    applicant_phone = Column(String(20), nullable=False)
    applicant_address = Column(String(255), nullable=False)
    applicant_id_number = Column(String(20), nullable=False)
    housing_type = Column(String(20))
    has_other_pets = Column(Boolean, default=False)
    adoption_reason = Column(Text, nullable=False)
    experience_description = Column(Text)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    pet = relationship("AdoptablePet", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
    review_records = relationship("ReviewRecord", back_populates="application")
    visit_reminders = relationship("VisitReminder", back_populates="application")
