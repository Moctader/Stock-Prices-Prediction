import pytest
from services.data_rmse_service import DataRMSEService


def test_get_rmse():
    service = DataRMSEService()
    rmse = service.get_rmse()
    assert isinstance(rmse, float)
    assert rmse >= 0
