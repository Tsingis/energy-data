from datetime import datetime
from pydantic import BaseModel, RootModel
from typing import List, Dict, Optional


class EnergyApiResponse(BaseModel):
    datasetId: int
    value: float  # Unit: MW
    startTime: str  # YYYY-MM-DDThh:mm:ss.fffZ
    endTime: Optional[str] = None  # YYYY-MM-DDThh:mm:ss.fffZ

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)


class Energy(BaseModel):
    timestamp: datetime
    value: float  # Unit: MW

    @classmethod
    def from_api_response(cls, api: EnergyApiResponse) -> "Energy":
        return cls(timestamp=datetime.fromisoformat(api.startTime), value=api.value)


class EnergyResponse(RootModel[Dict[str, List[Energy]]]):
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)
