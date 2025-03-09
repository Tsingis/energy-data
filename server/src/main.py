import logging
import os
import uvicorn
from aiocache import SimpleMemoryCache
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from energy_client import EnergyClient, EnergyData
from price_client import PriceClient, PriceData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = SimpleMemoryCache()

now = datetime.now(timezone.utc)
delta = timedelta(hours=12)
start_time = now - delta
end_time = now + delta


@app.get("/data/energy")
async def get_energy_data():
    try:
        cache_key = "main:data:energy"
        cached_value = await cache.get(cache_key)
        if cached_value:
            data = EnergyData.model_validate_json(cached_value)
            return data.model_dump()

        client = EnergyClient()
        data = await client.fetch_energy_data(start_time, end_time)

        await cache.set(cache_key, data.model_dump(), ttl=int(os.getenv("CACHE_TTL", 900)))
        return data.model_dump()
    except Exception:
        logger.exception("Error fetching energy data")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching energy data",
        )


@app.get("/data/price")
async def get_price_data():
    try:
        cache_key = "main:data:price"
        cached_value = await cache.get(cache_key)
        if cached_value:
            data = PriceData.model_validate_json(cached_value)
            return data.model_dump()

        client = PriceClient()
        data = await client.fetch_price_data(start_time, end_time)

        await cache.set(cache_key, data.model_dump(), ttl=int(os.getenv("CACHE_TTL", 900)))
        return data.model_dump()
    except Exception:
        logger.exception("Error fetching price data")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching price data",
        )


@app.get("/health")
def health():
    return {"message": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
