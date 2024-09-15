import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.models.stock_price import StockPrice
from app.db.session import SessionLocal

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    from app.db.base import Base
    from app.db.session import engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_ingest_data(test_db):
    response = client.post("/api/v1/ingest", json={"code": "AAPL"})
    assert response.status_code == 200
    assert response.json()["message"] == "Data ingested successfully"


def test_get_all_ingested_data(test_db):
    response = client.get(
        "/api/v1/ingest", params={"page": 1, "page_size": 10})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "code" in data[0]
    assert data[0]["code"] == "AAPL"
