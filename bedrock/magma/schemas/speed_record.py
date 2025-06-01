from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict, validator
from typing import List, Optional, Literal
from datetime import datetime, timezone


# ########    PYDANTIC SCHEMA:  speed_record    ########


# -------- Base schema shared across input/output --------
class SpeedRecordBase(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the speed record.")
    speed: float = Field(..., ge=0, description="Speed must be non-negative.")
    link_id: int = Field(..., description="Identifier of the associated Link.")


# -------- Used for incoming POST data (example: new LinkStringGeometry) --------
class SpeedRecordCreate(SpeedRecordBase):

    # TODO: Elsewhere in Bedrock, change to using validate_by_name and validate_by_alias over populate_by_name
    model_config = ConfigDict(extra="forbid", validate_by_name=True, validate_by_alias=True)


# -------- Used for response serialization (example: API GET /links/1) --------
class SpeedRecordRead(SpeedRecordBase):
    id: int

    class Config:
        from_attributes = True

