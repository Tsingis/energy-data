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

        self.assertIn(str(Dataset.PRODUCTION.value), result)
        self.assertIn(str(Dataset.CONSUMPTION.value), result)

        production_data = result[str(Dataset.PRODUCTION.value)]
        self.assertEqual(2, len(production_data))
        self.assertEqual(
            datetime.fromisoformat("2025-03-20T10:00:00"), production_data[0].timestamp
        )
        self.assertEqual(100.0, production_data[0].value)
        self.assertEqual(
            datetime.fromisoformat("2025-03-20T11:00:00"), production_data[1].timestamp
        )
        self.assertEqual(110.0, production_data[1].value)

        consumption_data = result[str(Dataset.CONSUMPTION.value)]
        self.assertEqual(1, len(consumption_data))
        self.assertEqual(
            datetime.fromisoformat("2025-03-20T10:00:00"), consumption_data[0].timestamp
        )
        self.assertEqual(200.0, consumption_data[0].value)

    def test_adjust_predictions_production(self):
        data = {
            str(Dataset.PRODUCTION.value): [EnergyModel(timestamp=self.last_time, value=100.0)],
            str(Dataset.PRODUCTION_PREDICTION.value): [
                EnergyModel(timestamp=self.last_time - timedelta(hours=2), value=90.0),
                EnergyModel(timestamp=self.last_time + timedelta(hours=1), value=110.0),
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[str(Dataset.PRODUCTION_PREDICTION.value)]))
        self.assertEqual(
            self.last_time + timedelta(hours=1),
            data[str(Dataset.PRODUCTION_PREDICTION.value)][0].timestamp,
        )
        self.assertEqual(110.0, data[str(Dataset.PRODUCTION_PREDICTION.value)][0].value)

    def test_adjust_predictions_consumption(self):
        data = {
            str(Dataset.CONSUMPTION.value): [EnergyModel(timestamp=self.last_time, value=200.0)],
            str(Dataset.CONSUMPTION_PREDICTION.value): [
                EnergyModel(timestamp=self.last_time - timedelta(hours=2), value=190.0),
                EnergyModel(timestamp=self.last_time + timedelta(hours=1), value=210.0),
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[str(Dataset.CONSUMPTION_PREDICTION.value)]))
        self.assertEqual(
            self.last_time + timedelta(hours=1),
            data[str(Dataset.CONSUMPTION_PREDICTION.value)][0].timestamp,
        )
        self.assertEqual(210.0, data[str(Dataset.CONSUMPTION_PREDICTION.value)][0].value)

    def test_adjust_predictions_no_adjustment(self):
        data = {
            str(Dataset.PRODUCTION.value): [EnergyModel(timestamp=datetime.now(), value=100.0)],
            str(Dataset.CONSUMPTION_PREDICTION.value): [
                EnergyModel(timestamp=datetime.now() + timedelta(hours=1), value=200.0)
            ],
        }

        self.client._adjust_predictions(data)

        self.assertEqual(1, len(data[str(Dataset.PRODUCTION.value)]))
        self.assertEqual(1, len(data[str(Dataset.CONSUMPTION_PREDICTION.value)]))
        self.assertEqual(100.0, data[str(Dataset.PRODUCTION.value)][0].value)
        self.assertEqual(200.0, data[str(Dataset.CONSUMPTION_PREDICTION.value)][0].value)


if __name__ == "__main__":
    unittest.main()
