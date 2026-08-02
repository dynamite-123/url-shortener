from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class CreateURLRequest(BaseModel):
    original_url: HttpUrl
    expires_at: datetime | None = None


class UpdateExpirationRequest(BaseModel):
    expires_at: datetime | None = None


class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: datetime | None
    click_count: int
    is_active: bool