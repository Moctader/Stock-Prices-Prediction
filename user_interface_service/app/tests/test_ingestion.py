import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.models.financial_data import FinancialData

client = TestClient(app)

def test_ingest_data(test_db):
    response = client.post("/api/v1/ingest", json={"code": "AAPL"})
    assert response.status_code == 200
    assert response.json()["message"] == "Data ingested successfully"

    data = test_db.query(FinancialData).filter(FinancialData.code == "AAPL").first()
    assert data is not None
    assert data.code == "AAPL"
