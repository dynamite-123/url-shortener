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


if __name__ == "__main__":
    import asyncio
    import sys

    from app.core.config import settings

    async def main():
        token = sys.argv[1] if len(sys.argv) > 1 else "your_token_here"
        print(f"Verifying token: {token}")

        async with AsyncClient(base_url=settings.auth_service_url, timeout=5.0) as http_client:
            client = AuthClient(http_client)
            user = await client.verify_token(token)
            print(f"Token is valid. User info: {user}")

    asyncio.run(main())