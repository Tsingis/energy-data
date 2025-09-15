import httpx
import os
import urllib.parse
from datetime import datetime
from typing import List, Dict
from enums.dataset import Dataset
from models.energy import Energy, EnergyApiResponse, EnergyResponse


class EnergyService:
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

    async def fetch_energy_data(self, start_time: datetime, end_time: datetime) -> EnergyResponse:
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
            response.raise_for_status()
            data = response.json()
            api_energy = [EnergyApiResponse.model_validate_json(x) for x in data.get("data", [])]
            energy = self._to_response_model(api_energy)
            self._adjust_predictions(energy)
            return EnergyResponse(energy)

    def _to_response_model(self, energy_data: List[EnergyApiResponse]) -> Dict[str, List[Energy]]:
        data: Dict[str, List[Energy]] = {}
        for item in energy_data:
            dataset_id = str(item.datasetId)
            dataset_key = self.dataset_mapping[dataset_id]
            energy_item = Energy.from_api_response(item)
            if dataset_key not in data:
                data[dataset_key] = []
            data[dataset_key].append(energy_item)
        return data

    def _adjust_predictions(self, data: Dict[str, List[Energy]]) -> None:
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
