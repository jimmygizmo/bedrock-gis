from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  link    ########


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    # For this LineString gemoetry, srid=4326 specifies GPS lattitude/longitude (lat/lon) format
    geom = Column(Geometry("LineString", srid=4326), nullable=False)

    # Relationship: one Link to many SpeedRecords
    speed_records = relationship("SpeedRecord", back_populates="link")

