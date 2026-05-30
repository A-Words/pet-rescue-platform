from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class FoundClue(Base):
    __tablename__ = "found_clues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    lost_pet_id = Column(UUID(as_uuid=True), ForeignKey("lost_pets.id"), nullable=False)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    photo_urls = Column(ARRAY(String))
    description = Column(Text, nullable=False)
    found_location = Column(String(255), nullable=False)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    found_date = Column(Date, nullable=False)
    contact_info = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    admin_notes = Column(Text)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reviewed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    lost_pet = relationship("LostPet", back_populates="clues")
    reporter = relationship("User", back_populates="found_clues", foreign_keys=[reporter_id])
