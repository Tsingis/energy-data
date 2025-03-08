import httpx
import os
import urllib.parse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from enum import Enum
from pydantic import BaseModel
from typing import List, Dict

load_dotenv()


class EnergyModel(BaseModel):
    timestamp: datetime
    value: float


class EnergyData(BaseModel):
    data: Dict[str, List[EnergyModel]]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)


class Dataset(Enum):
    PRODUCTION = 74
    PRODUCTION_PREDICTION = 241
    CONSUMPTION = 193
    CONSUMPTION_PREDICTION = 165


class EnergyClient:
    def __init__(self):
        self.api_key = os.getenv("FINGRID_API_KEY")
        self.base_url = "https://data.fingrid.fi/api/data"
        self.datasets = [
            Dataset.PRODUCTION.value,
            Dataset.PRODUCTION_PREDICTION.value,
            Dataset.CONSUMPTION.value,
            Dataset.CONSUMPTION_PREDICTION.value,
        ]
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    async def fetch_energy_data(self) -> EnergyData:
        now = datetime.now(timezone.utc)
        params = {
            "datasets": ",".join(map(str, self.datasets)),
            "pageSize": 1000,
            "startTime": (now + timedelta(hours=-12)).strftime(self.datetime_format),
            "endTime": (now + timedelta(hours=1)).strftime(self.datetime_format),
            "format": "json",
            "sortBy": "startTime",
            "sortOrder": "asc",
        }
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = self._map_response_to_model(response.json())
                return EnergyData(data=data)
            response.raise_for_status()

    def _map_response_to_model(self, json: Dict) -> Dict[str, List[EnergyModel]]:
        data = {}
        for item in json.get("data", []):
            dataset_id = str(item["datasetId"])
            time = datetime.strptime(item["startTime"], self.datetime_format)

            data_point = EnergyModel(timestamp=time, value=item["value"])
            if dataset_id not in data:
                data[dataset_id] = []
            data[dataset_id].append(data_point)
        return data
