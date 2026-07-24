from datetime import datetime

from pydantic import BaseModel, RootModel


class PriceApiResponse(BaseModel):
    price: float  # Unit: c/kWh
    startDate: str  # YYYY-MM-DDThh:mm:ss.fffZ
    endDate: str | None = None  # YYYY-MM-DDThh:mm:ss.fffZ

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)


class Price(BaseModel):
    timestamp: datetime
    value: float  # c/kWh

    @classmethod
    def from_api_response(cls, api: PriceApiResponse) -> "Price":
        return cls(timestamp=datetime.fromisoformat(api.startDate), value=api.price)


class PriceResponse(RootModel[list[Price]]):
    class Config:
        def __init__(self):
            self.json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def model_validate_json(cls, json_data):
        return cls.model_validate(json_data)
