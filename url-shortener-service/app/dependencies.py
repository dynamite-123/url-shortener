from fastapi import Depends, Header, HTTPException, Request, status

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from app.core.database import SessionLocal
from app.schemas.auth import VerifyTokenResponse
from app.services.auth_client import AuthClient


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_auth_client(request: Request) -> AuthClient:
    return request.app.state.auth_client


async def get_current_user(
    authorization: str = Header(...),
    auth_client: AuthClient = Depends(get_auth_client),
) -> VerifyTokenResponse:
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )
    token = authorization[7:]

    try:
        user = await auth_client.verify_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user
