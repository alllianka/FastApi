from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AdvertisementBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    price: float = Field(..., ge=0)
    author: str = Field(..., max_length=255)


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    author: Optional[str] = Field(None, max_length=255)


class AdvertisementResponse(AdvertisementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime