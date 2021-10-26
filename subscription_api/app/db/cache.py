from typing import AsyncIterator

import aioredis
from aioredis import Redis

from app.core.config import settings


async def get_cache() -> AsyncIterator[Redis]:
    pool = await aioredis.create_redis_pool((settings.cache.host, settings.cache.port))
    yield pool
    pool.close()
    await pool.wait_closed()
