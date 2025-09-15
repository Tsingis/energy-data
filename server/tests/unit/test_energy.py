import unittest
from datetime import datetime, timedelta, timezone
from src.enums.dataset import Dataset
from src.models.energy import Energy, EnergyApiResponse
from src.services.energy_service import EnergyService


class TestEnergy(unittest.TestCase):
    def setUp(self):
        self.client = EnergyService()
        self.last_time = datetime.now() - timedelta(hours=1)

    def test_from_api_response_mapping(self):
        api = EnergyApiResponse(datasetId=1, startTime="2025-03-20T10:00:00.000Z", value=5.0)
        energy = Energy.from_api_response(api)

        self.assertEqual(datetime(2025, 3, 20, 10, 0, 0, 0, tzinfo=timezone.utc), energy.timestamp)
        self.assertEqual(5.0, energy.value)

    def test_to_response_model(self):
        api_response = [
            EnergyApiResponse(
                datasetId=Dataset.PRODUCTION.value, startTime="2025-03-20T10:00:00Z", value=100.0
            ),
            EnergyApiResponse(
                datasetId=Dataset.PRODUCTION.value, startTime="2025-03-20T11:00:00Z", value=110.0
            ),
            EnergyApiResponse(
                datasetId=Dataset.CONSUMPTION.value, startTime="2025-03-20T10:00:00Z", value=200.0
            ),
        ]

        result = self.client._to_response_model(api_response)

        self.assertIn(Dataset.PRODUCTION.key_name, result)
        self.assertIn(Dataset.CONSUMPTION.key_name, result)

        production_data = result[Dataset.PRODUCTION.key_name]
        self.assertEqual(2, len(production_data))
        self.assertEqual(
            datetime(2025, 3, 20, 10, 0, 0, tzinfo=timezone.utc), production_data[0].timestamp
        )
        self.assertEqual(100.0, production_data[0].value)
        self.assertEqual(
            datetime(2025, 3, 20, 11, 0, 0, tzinfo=timezone.utc), production_data[1].timestamp
        )
        self.assertEqual(110.0, production_data[1].value)

        consumption_data = result[Dataset.CONSUMPTION.key_name]
        self.assertEqual(1, len(consumption_data))
        self.assertEqual(
            datetime(2025, 3, 20, 10, 0, 0, tzinfo=timezone.utc), consumption_data[0].timestamp
        )
        self.assertEqual(200.0, consumption_data[0].value)

    def test_adjust_predictions_production(self):
        data = {
            Dataset.PRODUCTION.key_name: [Energy(timestamp=self.last_time, value=100.0)],
            Dataset.PRODUCTION_PREDICTION.key_name: [
                Energy(timestamp=self.last_time - timedelta(hours=2), value=90.0),
                Energy(timestamp=self.last_time + timedelta(hours=1), value=110.0),
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[Dataset.PRODUCTION_PREDICTION.key_name]))
        self.assertEqual(
            self.last_time + timedelta(hours=1),
            data[Dataset.PRODUCTION_PREDICTION.key_name][0].timestamp,
        )
        self.assertEqual(110.0, data[Dataset.PRODUCTION_PREDICTION.key_name][0].value)

    def test_adjust_predictions_consumption(self):
        data = {
            Dataset.CONSUMPTION.key_name: [Energy(timestamp=self.last_time, value=200.0)],
            Dataset.CONSUMPTION_PREDICTION.key_name: [
                Energy(timestamp=self.last_time - timedelta(hours=2), value=190.0),
                Energy(timestamp=self.last_time + timedelta(hours=1), value=210.0),
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[Dataset.CONSUMPTION_PREDICTION.key_name]))
        self.assertEqual(
            self.last_time + timedelta(hours=1),
            data[Dataset.CONSUMPTION_PREDICTION.key_name][0].timestamp,
        )
        self.assertEqual(210.0, data[Dataset.CONSUMPTION_PREDICTION.key_name][0].value)

    def test_adjust_predictions_no_adjustment(self):
        data = {
            Dataset.PRODUCTION.key_name: [Energy(timestamp=datetime.now(), value=100.0)],
            Dataset.CONSUMPTION_PREDICTION.key_name: [
                Energy(timestamp=datetime.now() + timedelta(hours=1), value=200.0)
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[Dataset.PRODUCTION.key_name]))
        self.assertEqual(1, len(data[Dataset.CONSUMPTION_PREDICTION.key_name]))
        self.assertEqual(100.0, data[Dataset.PRODUCTION.key_name][0].value)
        self.assertEqual(200.0, data[Dataset.CONSUMPTION_PREDICTION.key_name][0].value)


if __name__ == "__main__":
    unittest.main()
