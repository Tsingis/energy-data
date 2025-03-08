import logging
import uvicorn
from aiocache import SimpleMemoryCache
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from energy_client import EnergyClient, EnergyData

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


@app.get("/data")
async def get_data():
    try:
        cache_key = "main:data"
        cached_value = await cache.get(cache_key)
        if cached_value:
            data = EnergyData.model_validate_json(cached_value)
            return data.model_dump()

        client = EnergyClient()
        data = await client.fetch_energy_data()

        await cache.set(cache_key, data.model_dump(), ttl=900)
        return data.model_dump()
    except Exception:
        logger.exception("Error fetching data")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching data",
        )


@app.get("/health")
def health():
    return {"message": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
