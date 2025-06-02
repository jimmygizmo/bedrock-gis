from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict, validator
from typing import List, Optional, Literal
from datetime import datetime, timezone


# ########    PYDANTIC SCHEMA:  speed_record    ########


# -------- Base schema shared across input/output --------
class SpeedRecordBase(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the speed record.")
    # Aliases that match seed data column names can assist importing. TODO: Consider this when we get to import code.
    # timestamp: datetime = Field(..., alias="timeStamp", description="Timestamp of the speed record.")
    speed: float = Field(..., ge=0, description="Speed must be non-negative.")
    link_id: int = Field(..., description="Identifier of the associated Link.")
    # Test this shared model_config before using it.
    # We use different parts of it below. Common should work fine, but test it!
    #
    # model_config = ConfigDict(
    #     extra="forbid",
    #     validate_by_name=True,
    #     validate_by_alias=True,
    #     from_attributes=True
    # )
    #
    # And if we need to modify the field names for output. Remember we can customize/extend the base model_config.
    # model_config = ConfigDict(serialize_by_alias=True)


# -------- Used for incoming POST data (example: new LinkStringGeometry) --------
class SpeedRecordCreate(SpeedRecordBase):

    # TODO: Elsewhere in Bedrock, change to using validate_by_name and validate_by_alias over populate_by_name
    model_config = ConfigDict(extra="forbid", validate_by_name=True, validate_by_alias=True)


# -------- Used for response serialization (example: API GET /links/1) --------
class SpeedRecordRead(SpeedRecordBase):
    id: int

    class Config:
        from_attributes = True

