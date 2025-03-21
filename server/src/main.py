import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from datetime import datetime, timedelta, timezone
from common.setup_logger import setup_logger
from common.cache import cache_result
from common.exception_handlers import (
    http_exception_handler,
    fastapi_http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    ratelimit_exception_handler,
)
from middleware.secure_headers import SecureHeadersMiddleware
from clients.energy_client import EnergyClient, EnergyData
from clients.price_client import PriceClient, PriceData


ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:3000")
CACHE_TTL = int(os.getenv("CACHE_TTL", 900))

logger = setup_logger()

app = FastAPI()

limiter = Limiter(key_func=lambda: "global")
app.state.limiter = limiter

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(HTTPException, fastapi_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RateLimitExceeded, ratelimit_exception_handler)

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


@app.get("/data/energy", response_model=EnergyData)
@limiter.limit("10/minute")
@cache_result(cache_key="main:data:energy", model_type=EnergyData, ttl=CACHE_TTL)
async def get_energy_data(request: Request):
    client = EnergyClient()
    data = await client.fetch_energy_data(start_time, end_time)
    return data.model_dump()


@app.get("/data/price", response_model=PriceData)
@limiter.limit("10/minute")
@cache_result(cache_key="main:data:price", model_type=PriceData, ttl=CACHE_TTL)
async def get_price_data(request: Request):
    client = PriceClient()
    data = await client.fetch_price_data(start_time, end_time)
    return data.model_dump()


@app.get("/health", include_in_schema=False)
@limiter.limit("30/minute")
def health(request: Request):
    return {"message": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT", "dev").lower() == "dev"
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_config=None, reload=reload)
