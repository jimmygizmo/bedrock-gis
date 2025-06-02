from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  slink    ########


class Slink(Base):
    __tablename__ = "slinks"

    # id = Column("link_id", Integer, primary_key=True, index=True)  # __name_pos will cutomize the col name
    id = Column(Integer, primary_key=True, index=True)

    _length = Column(Float)  # Converted from object to float
    road_name = Column(String)
    usdk_speed_category = Column(Integer)
    funclass_id = Column(Integer)
    speedcat = Column(Integer)
    volume_value = Column(Integer)
    volume_bin_id = Column(Integer)
    volume_year = Column(Integer)
    volumes_bin_description = Column(String)

    # For this LineString gemoetry, srid=4326 specifies GPS lattitude/longitude (lat/lon) format
    geometry = Column(Geometry("MultiLineString", srid=4326), nullable=False)

    # Note the back_populates="slink" is singular and this is intentional to match the LINK declared in SspeedRecord
    # One might assume this was meant to refer to the table name and this be plural but I AM NEARLY POSITIVE THATS WRONG.
    # TODO: Test this. We will know when we get this all working.
    sspeed_records = relationship("SspeedRecord", back_populates="slink")


###################################
# - - - - SHAPE ---- df.shape - - - - - - - - - - - - - - - - - - - - - - -
# SHAPE: (100924, 11)
# - - - - DTYPES ---- df.dtypes - - - - - - - - - - - - - - - - - - - - - - -
# SHAPE: link_id                     int64
# _length                    object
# road_name                  object
# usdk_speed_category         int64
# funclass_id                 int64
# speedcat                    int64
# volume_value                int64
# volume_bin_id               int64
# volume_year                 int64
# volumes_bin_description    object
# geo_json                   object
# dtype: object

