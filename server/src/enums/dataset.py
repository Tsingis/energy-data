from enum import Enum


class Dataset(Enum):
    PRODUCTION = 74
    PRODUCTION_PREDICTION = 241
    CONSUMPTION = 193
    CONSUMPTION_PREDICTION = 165

    @property
    def key_name(self) -> str:
        return self.name.lower()
