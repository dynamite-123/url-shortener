from app.utils.base62 import encode_base62
from redis.asyncio import Redis

SECRET_MULTIPLIER = 79195719

async def create_short_code(redis: Redis) -> tuple[int, str]:
    counter = await redis.incr("global:id")

    obfuscated = (counter * SECRET_MULTIPLIER) & 0xFFFFFFFFFFFFFFFF
    short_code = encode_base62(obfuscated)

    return counter, short_code