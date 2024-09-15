import pytest
from services.data_prediction_service import DataPredictionService


def test_get_predictions():
    service = DataPredictionService()
    predictions = service.get_predictions()
    assert isinstance(predictions, list)
    assert len(predictions) > 0
    assert isinstance(predictions[0], float)


def test_get_test_and_pred():
    service = DataPredictionService()
    y_test, y_pred = service.get_test_and_pred()
    assert isinstance(y_test, list)
    assert isinstance(y_pred, list)
    assert len(y_test) == len(y_pred)
    assert isinstance(y_test[0], float)
    assert isinstance(y_pred[0], float)
