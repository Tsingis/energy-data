from datetime import datetime

import httpx

from src.models.price import Price, PriceApiResponse, PriceResponse


class PriceService:
    def __init__(self):
        self.base_url = "https://api.porssisahko.net/v2/latest-prices.json"

    async def fetch_price_data(self, start_time: datetime, end_time: datetime) -> PriceResponse:
        """
        Fetches prices in cents / kWh
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            response.raise_for_status()
            data = response.json()
            api_prices = [PriceApiResponse.model_validate_json(x) for x in data.get("prices", [])]
            prices = [Price.from_api_response(x) for x in api_prices]
            filtered = self._filter_data_by_time(prices, start_time, end_time)
            return PriceResponse(filtered)

    def _filter_data_by_time(
        self, data: list[Price], start_time: datetime, end_time: datetime
    ) -> list[Price]:
        return [item for item in data if start_time <= item.timestamp <= end_time]
