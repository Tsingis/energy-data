import unittest
from datetime import datetime, timedelta
from src.clients.price_client import PriceClient, PriceModel


class TestPriceClient(unittest.TestCase):
    def setUp(self):
        self.client = PriceClient()
        self.start_time = datetime.now() - timedelta(hours=2)
        self.end_time = datetime.now()

    def test_map_response_to_model(self):
        mock_json = {
            "prices": [
                {
                    "startDate": "2025-03-20T10:00:00",
                    "price": 5.0,
                },
                {
                    "startDate": "2025-03-20T11:00:00",
                    "price": 6.5,
                },
            ]
        }

        result = self.client._map_response_to_model(mock_json)

        self.assertEqual(2, len(result))
        self.assertEqual(datetime.fromisoformat("2025-03-20T10:00:00"), result[0].timestamp)
        self.assertEqual(5.0, result[0].value)
        self.assertEqual(datetime.fromisoformat("2025-03-20T11:00:00"), result[1].timestamp)
        self.assertEqual(6.5, result[1].value)

    def test_filter_data_by_time(self):
        data = [
            PriceModel(timestamp=self.start_time - timedelta(hours=1), value=4.0),
            PriceModel(timestamp=self.start_time + timedelta(minutes=30), value=5.0),
            PriceModel(timestamp=self.end_time - timedelta(minutes=30), value=6.0),
            PriceModel(timestamp=self.end_time + timedelta(hours=1), value=7.0),
        ]

        filtered_data = self.client._filter_data_by_time(data, self.start_time, self.end_time)

        self.assertEqual(2, len(filtered_data))
        self.assertEqual(self.start_time + timedelta(minutes=30), filtered_data[0].timestamp)
        self.assertEqual(5.0, filtered_data[0].value)
        self.assertEqual(self.end_time - timedelta(minutes=30), filtered_data[1].timestamp)
        self.assertEqual(6.0, filtered_data[1].value)


if __name__ == "__main__":
    unittest.main()
