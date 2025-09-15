from typing import Type
from aiocache import SimpleMemoryCache
from functools import wraps
from fastapi import HTTPException, status
from .setup_logger import setup_logger

logger = setup_logger()

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
                if isinstance(result, list):
                    result = model_type(result)
                else:
                    result = model_type(**result)
                await cache.set(cache_key, result, ttl=ttl)
                return result
            except Exception:
                logger.exception("Error in caching for key %s", cache_key)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error processing request",
                )

        return wrapper

    return decorator
