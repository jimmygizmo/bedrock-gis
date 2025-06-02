from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict, validator
from typing import List, Optional, Literal, Tuple

# TODO: Consider using:
# from geojson_pydantic import LineString
# Might be better to use this rather than the custom approach we have initially. For typing and validation


# ########    PYDANTIC SCHEMA:  link    ########


# -------- Base schema shared across input/output --------
# GeoJSON format
class LineStringGeometryBase(BaseModel):
    type: Literal["LineString"]
    coordinates: List[Tuple[float, float]]  # List of [latttitude, longitude] pairs


# -------- Used for incoming POST data (example: new LinkStringGeometry) --------
class LineStringGeometryCreate(LineStringGeometryBase):

    model_config = ConfigDict(extra="forbid", validate_by_name=True, validate_by_alias=True)

# -------- Used for response serialization (example: API GET /links/1) --------
class LineStringGeometryRead(LineStringGeometryBase):
    id: int

    class Config:
        from_attributes = True

    # Old style validator - now deprecated. Still useful but TODO: Modernize this validation. It is a good check.
    # @validator("coordinates", each_item=True)
    # def validate_coordinates(cls, coord):
    #     lon, lat = coord
    #     if not (-180 <= lon <= 180):
    #         raise ValueError("Longitude must be between -180 and 180 degrees.")
    #     if not (-90 <= lat <= 90):
    #         raise ValueError("Latitude must be between -90 and 90 degrees.")
    #     return coord

