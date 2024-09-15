import pytest
from service import Svc


@pytest.mark.asyncio
async def test_get_inference():
    service = Svc()
    result = await service.get_inference()
    assert "data_head" in result
    assert "predictions" in result
    assert "rmse" in result
    assert isinstance(result["data_head"], list)
    assert isinstance(result["predictions"], list)
    assert isinstance(result["rmse"], float)
