import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from setup_logger import setup_logger
from cache import cache_result
from middleware.secure_headers import SecureHeadersMiddleware
from energy_client import EnergyClient, EnergyData
from price_client import PriceClient, PriceData


ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:3000")
CACHE_TTL = int(os.getenv("CACHE_TTL", 900))

logger = setup_logger()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["Accept", "Content-Type"],
)

app.add_middleware(SecureHeadersMiddleware)

now = datetime.now(timezone.utc)
delta = timedelta(hours=24)
start_time = now - delta
end_time = now + delta


@app.get("/data/energy")
@cache_result(cache_key="main:data:energy", model_type=EnergyData, ttl=CACHE_TTL)
async def get_energy_data():
    client = EnergyClient()
    data = await client.fetch_energy_data(start_time, end_time)
    return data.model_dump()


@app.get("/data/price")
@cache_result(cache_key="main:data:price", model_type=PriceData, ttl=CACHE_TTL)
async def get_price_data():
    client = PriceClient()
    data = await client.fetch_price_data(start_time, end_time)
    return data.model_dump()


@app.get("/health")
def health():
    return {"message": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT", "dev") == "dev"
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_config=None, reload=reload)
