from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict


class CreateURLRequest(BaseModel):
    original_url: HttpUrl
    expires_at: datetime | None = None


class UpdateURLRequest(BaseModel):
    original_url: HttpUrl | None = None
    expires_at: datetime | None = None
    is_active: bool | None = None


class URLResponse(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: datetime | None
    click_count: int
    is_active: bool


class URLStatsResponse(BaseModel):
    short_code: str
    click_count: int
    created_at: datetime
    expires_at: datetime | None


class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: datetime | None
    click_count: int
    is_active: bool