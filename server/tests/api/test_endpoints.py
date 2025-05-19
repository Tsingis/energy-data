# flake8: noqa: E402

import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from src.main import app
from src.clients.energy_client import Dataset


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "healthy"})

    def test_get_energy_data(self):
        response = self.client.get("/api/energy")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn(Dataset.PRODUCTION.key_name, data)
        self.assertIn(Dataset.PRODUCTION_PREDICTION.key_name, data)
        self.assertIn(Dataset.CONSUMPTION.key_name, data)
        self.assertIn(Dataset.CONSUMPTION_PREDICTION.key_name, data)

    def test_get_price_data(self):
        response = self.client.get("/api/price")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
