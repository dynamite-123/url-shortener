from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import Redis

from app.core.config import settings
from app.core.database import Base, engine
from app.services.auth_client import AuthClient

# Import models so SQLAlchemy registers them before create_all
import app.models.url  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables if they don't exist yet
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    http_client = AsyncClient(
        base_url=settings.auth_service_url,
        timeout=5.0,
    )

    redis = Redis.from_url(
        settings.redis_url,
        decode_responses=True,
    )

    app.state.auth_client = AuthClient(http_client)
    app.state.redis = redis

    yield

    await http_client.aclose()
    await redis.aclose()