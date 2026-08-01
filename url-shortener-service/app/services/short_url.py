from app.utils.base62 import encode_base62
from redis.asyncio import Redis

async def create_short_code(redis: Redis) -> str:
    counter = await redis.incr("global_counter")
    return encode_base62(counter)
