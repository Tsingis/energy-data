import httpx
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict

load_dotenv()


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

    async def fetch_price_data(self) -> PriceData:
        """
        Fetches prices in cents / kWh
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            if response.status_code == 200:
                data = self._map_response_to_model(response.json())
                return PriceData(data=data)
            response.raise_for_status()

    def _map_response_to_model(self, json: Dict) -> Dict[str, List[PriceModel]]:
        data = []
        for item in json.get("prices", []):
            time = datetime.fromisoformat(item["startDate"])
            data_point = PriceModel(timestamp=time, value=item["price"])
            data.append(data_point)
        return data
