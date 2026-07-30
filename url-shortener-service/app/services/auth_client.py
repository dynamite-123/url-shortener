from httpx import AsyncClient

from app.schemas.auth import VerifyTokenResponse


class AuthClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def verify_token(self, token: str) -> VerifyTokenResponse:
        response = await self.client.post(
            "/api/auth/verify",
            json={"token": token},
        )

        response.raise_for_status()

        return VerifyTokenResponse.model_validate(response.json())