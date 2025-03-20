import httpx
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict


class PriceModel(BaseModel):
    timestamp: datetime
    value: float  # Unit: c/kWh


class PriceData(BaseModel):
    data: List[PriceModel]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)


class PriceClient:
    def __init__(self):
        self.api_key = ""
        self.base_url = "https://api.porssisahko.net/v1/latest-prices.json"
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    async def fetch_price_data(self, start_time: datetime, end_time: datetime) -> PriceData:
        """
        Fetches prices in cents / kWh
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            if response.status_code == 200:
                data = self._map_response_to_model(response.json())
                data = self._filter_data_by_time(data, start_time, end_time)
                return PriceData(data=data)
            response.raise_for_status()

    def _map_response_to_model(self, json: Dict) -> List[PriceModel]:
        data = []
        for item in json.get("prices", []):
            time = datetime.fromisoformat(item["startDate"])
            data_point = PriceModel(timestamp=time, value=item["price"])
            data.append(data_point)
        return data

    def _filter_data_by_time(
        self, data: List[PriceModel], start_time: datetime, end_time: datetime
    ) -> List[PriceModel]:
        return [item for item in data if start_time <= item.timestamp <= end_time]
