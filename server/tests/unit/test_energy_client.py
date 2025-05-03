import unittest
from datetime import datetime, timedelta
from src.clients.energy_client import EnergyClient, EnergyModel, Dataset


class TestEnergyClient(unittest.TestCase):
    def setUp(self):
        self.client = EnergyClient()
        self.last_time = datetime.now() - timedelta(hours=1)

    def test_map_response_to_model(self):
        mock_json = {
            "data": [
                {
                    "datasetId": Dataset.PRODUCTION.value,
                    "startTime": "2025-03-20T10:00:00",
                    "value": 100.0,
                },
                {
                    "datasetId": Dataset.PRODUCTION.value,
                    "startTime": "2025-03-20T11:00:00",
                    "value": 110.0,
                },
                {
                    "datasetId": Dataset.CONSUMPTION.value,
                    "startTime": "2025-03-20T10:00:00",
                    "value": 200.0,
                },
            ]
        }

        result = self.client._map_response_to_model(mock_json)

        self.assertIn(Dataset.PRODUCTION.key_name, result)
        self.assertIn(Dataset.CONSUMPTION.key_name, result)

        production_data = result[Dataset.PRODUCTION.key_name]
        self.assertEqual(2, len(production_data))
        self.assertEqual(
            datetime.fromisoformat("2025-03-20T10:00:00"), production_data[0].timestamp
        )
        self.assertEqual(100.0, production_data[0].value)
        self.assertEqual(
            datetime.fromisoformat("2025-03-20T11:00:00"), production_data[1].timestamp
        )
        self.assertEqual(110.0, production_data[1].value)

        consumption_data = result[Dataset.CONSUMPTION.key_name]
        self.assertEqual(1, len(consumption_data))
        self.assertEqual(
            datetime.fromisoformat("2025-03-20T10:00:00"), consumption_data[0].timestamp
        )
        self.assertEqual(200.0, consumption_data[0].value)

    def test_adjust_predictions_production(self):
        data = {
            Dataset.PRODUCTION.key_name: [EnergyModel(timestamp=self.last_time, value=100.0)],
            Dataset.PRODUCTION_PREDICTION.key_name: [
                EnergyModel(timestamp=self.last_time - timedelta(hours=2), value=90.0),
                EnergyModel(timestamp=self.last_time + timedelta(hours=1), value=110.0),
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
            Dataset.CONSUMPTION.key_name: [EnergyModel(timestamp=self.last_time, value=200.0)],
            Dataset.CONSUMPTION_PREDICTION.key_name: [
                EnergyModel(timestamp=self.last_time - timedelta(hours=2), value=190.0),
                EnergyModel(timestamp=self.last_time + timedelta(hours=1), value=210.0),
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
            Dataset.PRODUCTION.key_name: [EnergyModel(timestamp=datetime.now(), value=100.0)],
            Dataset.CONSUMPTION_PREDICTION.key_name: [
                EnergyModel(timestamp=datetime.now() + timedelta(hours=1), value=200.0)
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[Dataset.PRODUCTION.key_name]))
        self.assertEqual(1, len(data[Dataset.CONSUMPTION_PREDICTION.key_name]))
        self.assertEqual(100.0, data[Dataset.PRODUCTION.key_name][0].value)
        self.assertEqual(200.0, data[Dataset.CONSUMPTION_PREDICTION.key_name][0].value)


if __name__ == "__main__":
    unittest.main()
