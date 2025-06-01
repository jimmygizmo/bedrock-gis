from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from magma.core.database import Base
from datetime import datetime, timezone


# ########    SQLALCHEMY MODEL:  speed_record    ########


class SpeedRecord(Base):
    __tablename__ = "speed_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    speed = Column(Float, nullable=False)

    # Relationship: many SpeedRecords to one Link
    # link_id - The Link to which this SpeedRecord belongs
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)
    link = relationship("Link", back_populates="speed_records")

