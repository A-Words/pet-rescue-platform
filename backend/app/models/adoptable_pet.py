from uuid import uuid4

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class AdoptablePet(Base):
    __tablename__ = "adoptable_pets"

    adoptable_pet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    pet_name = Column(String(50), nullable=False)
    pet_type = Column(String(20), nullable=False)
    breed = Column(String(50))
    color = Column(String(30))
    gender = Column(String(10))
    age_months = Column(Integer)
    photo_urls = Column(ARRAY(String))
    description = Column(Text)
    health_status = Column(String(20), nullable=False, default="healthy")
    is_vaccinated = Column(Boolean, nullable=False, default=False)
    is_dewormed = Column(Boolean, nullable=False, default=False)
    is_sterilized = Column(Boolean, nullable=False, default=False)
    adoption_status = Column(String(20), nullable=False, default="available")
    rescue_station = Column(String(100))
    intake_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    applications = relationship("AdoptionApplication", back_populates="pet")
