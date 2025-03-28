from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestInsuranceEndpoints:
    def test_calculate_endpoint(self):
        payload = {
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "value": 35000.00,
            "deductible_percentage": 0.1,
            "broker_fee": 50.00
        }
        response = client.post("/api/v1/insurance/calculate", json=payload)
        assert response.status_code == 200
        assert "calculated_premium" in response.json()

    def test_invalid_year_endpoint(self):
        payload = {
            "make": "Toyota",
            "model": "Corolla",
            "year": 2050,
            "value": 35000.00,
            "deductible_percentage": 0.1,
            "broker_fee": 50.00
        }
        response = client.post("/api/v1/insurance/calculate", json=payload)
        assert response.status_code == 422
