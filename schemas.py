from pydantic import BaseModel, Field, field_validator
from typing import List

class MSISDNRequest(BaseModel):
    msisdn: List[str] = Field(..., min_length=1, example=["8801XXXXXXXXX"])
    #start_date: str = Field(..., example="2026-01-01")
    #end_date: str = Field(..., example="2026-01-31")

    @field_validator("msisdn")
    @classmethod
    def validate_msisdn(cls, v):
        if len(v) == 0:
            raise ValueError("At least one MSISDN required")
        if len(v) > 50:
            raise ValueError("Maximum 50 MSISDNs per request")
        return v

    #@field_validator("start_date", "end_date")
    #@classmethod
    #def validate_date(cls, v):
    #    import re
    #    if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
    #        raise ValueError("Date must be in YYYY-MM-DD format")
    #    return v