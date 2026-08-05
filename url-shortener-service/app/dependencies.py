from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from app.core.database import SessionLocal
from app.schemas.auth import VerifyTokenResponse, User  
from app.services.auth_client import AuthClient


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_auth_client(request: Request) -> AuthClient:
    return request.app.state.auth_client

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_client: AuthClient = Depends(get_auth_client),
) -> User:
    token = credentials.credentials
    try:
        response = await auth_client.verify_token(token)
        user = User(id=response.id, username=response.username, role=response.role)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user


