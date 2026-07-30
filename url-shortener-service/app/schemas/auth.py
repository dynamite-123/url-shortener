from pydantic import BaseModel


class VerifyTokenResponse(BaseModel):
    status: bool
    id: str
    username: str
    role: str