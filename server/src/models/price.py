from datetime import datetime
from pydantic import BaseModel, RootModel
from typing import List, Optional


class PriceApiResponse(BaseModel):
    price: float  # Unit: c/kWh
    startDate: str  # YYYY-MM-DDThh:mm:ss.fffZ
    endDate: Optional[str] = None  # YYYY-MM-DDThh:mm:ss.fffZ

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)


class Price(BaseModel):
    timestamp: datetime
    value: float  # c/kWh

    @classmethod
    def from_api_response(cls, api: PriceApiResponse) -> "Price":
        return cls(timestamp=datetime.fromisoformat(api.startDate), value=api.price)


class PriceResponse(RootModel[List[Price]]):
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)
