import httpx
import os
import urllib.parse
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, RootModel
from typing import List, Dict


class EnergyModel(BaseModel):
    timestamp: datetime
    value: float  # Unit: MW


class EnergyData(RootModel[Dict[str, List[EnergyModel]]]):
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

    @property
    def key_name(self) -> str:
        return self.name.lower()


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
        self.dataset_mapping = {str(dataset.value): dataset.key_name for dataset in Dataset}
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    async def fetch_energy_data(self, start_time: datetime, end_time: datetime) -> EnergyData:
        """
        Fetches energy consumptions, productions and their respective predictions in MW
        """
        params = {
            "datasets": ",".join(map(str, self.datasets)),
            "pageSize": 2000,
            "startTime": start_time.strftime(self.datetime_format),
            "endTime": end_time.strftime(self.datetime_format),
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
                self._adjust_predictions(data)
                return EnergyData(data)
            response.raise_for_status()

    def _map_response_to_model(self, json: Dict) -> Dict[str, List[EnergyModel]]:
        data = {}
        for item in json.get("data", []):
            dataset_id = str(item["datasetId"])
            dataset = self.dataset_mapping[dataset_id]
            time = datetime.fromisoformat(item["startTime"])
            data_point = EnergyModel(timestamp=time, value=item["value"])
            if dataset not in data:
                data[dataset] = []
            data[dataset].append(data_point)
        return data

    def _adjust_predictions(self, data: Dict[str, List[EnergyModel]]) -> None:
        if Dataset.PRODUCTION.key_name in data and Dataset.PRODUCTION_PREDICTION.key_name in data:
            last_production = data[Dataset.PRODUCTION.key_name][-1]
            # Remove predictions before the last production timestamp
            data[Dataset.PRODUCTION_PREDICTION.key_name] = [
                prediction
                for prediction in data[Dataset.PRODUCTION_PREDICTION.key_name]
                if prediction.timestamp >= last_production.timestamp
            ]

        if Dataset.CONSUMPTION.key_name in data and Dataset.CONSUMPTION_PREDICTION.key_name in data:
            last_consumption = data[Dataset.CONSUMPTION.key_name][-1]
            # Remove predictions before the last consumption timestamp
            data[Dataset.CONSUMPTION_PREDICTION.key_name] = [
                prediction
                for prediction in data[Dataset.CONSUMPTION_PREDICTION.key_name]
                if prediction.timestamp >= last_consumption.timestamp
            ]
