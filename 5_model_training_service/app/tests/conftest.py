import pytest
from services.data_broker_service import DataBrokerService
from services.data_prediction_service import DataPredictionService
from services.data_rmse_service import DataRMSEService


@pytest.fixture
def data_broker_service():
    return DataBrokerService()


@pytest.fixture
def data_prediction_service():
    return DataPredictionService()


@pytest.fixture
def data_rmse_service():
    return DataRMSEService()
