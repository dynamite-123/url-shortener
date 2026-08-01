from fastapi import Request

from redis.asyncio import Redis

from app.services.auth_client import AuthClient
from app.services.short_url import ShortURLService


def get_auth_client(request: Request) -> AuthClient:
    return request.app.state.auth_client


def get_redis(request: Request) -> Redis:
    return request.app.state.redis