from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class LostPet(Base):
    __tablename__ = "lost_pets"

    lost_pet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    pet_name = Column(String(50), nullable=False)
    pet_type = Column(String(20), nullable=False)
    breed = Column(String(50))
    color = Column(String(30))
    gender = Column(String(10))
    age_description = Column(String(50))
    photo_urls = Column(ARRAY(String))
    description = Column(Text, nullable=False)
    lost_date = Column(Date, nullable=False)
    lost_location = Column(String(255), nullable=False)
    rescue_station = Column(String(100))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    contact_info = Column(String(100), nullable=False)
    reward_amount = Column(Numeric(10, 2), default=0)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="lost_pets")
    clues = relationship("FoundClue", back_populates="lost_pet")
