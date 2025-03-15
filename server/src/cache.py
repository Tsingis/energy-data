from typing import Type
from aiocache import SimpleMemoryCache
from functools import wraps
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
cache = SimpleMemoryCache()


def cache_result(cache_key: str, model_type: Type, ttl: int = 900):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                cached_value = await cache.get(cache_key)
                if cached_value:
                    return model_type.model_validate_json(cached_value).model_dump()
                result = await func(*args, **kwargs)
                await cache.set(cache_key, model_type(**result).model_dump(), ttl=ttl)
                return result
            except Exception:
                logger.exception(f"Error in caching for key {cache_key}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error processing request",
                )

        return wrapper

    return decorator
