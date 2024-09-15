import pytest
from services.data_broker_service import DataBrokerService


def test_get_data_head():
    service = DataBrokerService()
    data_head = service.get_data_head()
    assert isinstance(data_head, list)
    assert len(data_head) > 0
    assert isinstance(data_head[0], dict)
