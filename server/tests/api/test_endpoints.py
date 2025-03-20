# flake8: noqa: E402

import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from src.main import app


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "healthy"})

    def test_get_energy_data(self):
        response = self.client.get("/data/energy")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

    def test_get_price_data(self):
        response = self.client.get("/data/price")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())


if __name__ == "__main__":
    unittest.main()
