import unittest
from datetime import datetime, timedelta, timezone
from src.models.price import Price, PriceApiResponse
from src.services.price_service import PriceService


class TestPrice(unittest.TestCase):
    def setUp(self):
        self.client = PriceService()
        self.start_time = datetime.now() - timedelta(hours=2)
        self.end_time = datetime.now()

    def test_from_api_response_mapping(self):
        api = PriceApiResponse(startDate="2025-03-20T10:00:00.000Z", price=5.0)
        price = Price.from_api_response(api)

        self.assertEqual(datetime(2025, 3, 20, 10, 0, 0, 0, tzinfo=timezone.utc), price.timestamp)
        self.assertEqual(5.0, price.value)

    def test_filter_data_by_time(self):
        data = [
            Price(timestamp=self.start_time - timedelta(hours=1), value=4.0),
            Price(timestamp=self.start_time + timedelta(minutes=30), value=5.0),
            Price(timestamp=self.end_time - timedelta(minutes=30), value=6.0),
            Price(timestamp=self.end_time + timedelta(hours=1), value=7.0),
        ]

        filtered_data = self.client._filter_data_by_time(data, self.start_time, self.end_time)

        self.assertEqual(2, len(filtered_data))
        self.assertEqual(self.start_time + timedelta(minutes=30), filtered_data[0].timestamp)
        self.assertEqual(5.0, filtered_data[0].value)
        self.assertEqual(self.end_time - timedelta(minutes=30), filtered_data[1].timestamp)
        self.assertEqual(6.0, filtered_data[1].value)


if __name__ == "__main__":
    unittest.main()
