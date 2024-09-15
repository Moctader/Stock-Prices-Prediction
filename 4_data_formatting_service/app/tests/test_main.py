from ..main import app
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json() == {"message": "Metrics endpoint"}


def test_home_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert str(response.url).endswith("/docs")
    assert response.history[0].status_code == 307


if __name__ == '__main__':
    pytest.main()
