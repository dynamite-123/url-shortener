from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import Redis

from app.core.config import settings
from app.services.auth_client import AuthClient


@asynccontextmanager
async def lifespan(app: FastAPI):
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