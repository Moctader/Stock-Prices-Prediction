import typing as t
import bentoml
from app.services.model_training_service import ModelTrainingService
from app.services.model_prediction_service import ModelPredictionService

SERVICE_NAME: str = "/model_training"
API_PREFIX: str = "/api/v1"


@bentoml.service()
class StartService():
    model_training_service = bentoml.depends(ModelTrainingService)
    model_prediction_service = bentoml.depends(ModelPredictionService)

    def __init__(self) -> None:
        print("The model training service has started")

    @bentoml.api(route=f"{API_PREFIX}{SERVICE_NAME}/train")
    def train_model(self) -> t.Dict[str, t.Any]:
        return self.model_training_service.train()

    @bentoml.api(route=f"{API_PREFIX}{SERVICE_NAME}/predict")
    def predict(self) -> t.List[float]:
        return self.model_prediction_service.predict()

    @bentoml.api(route=f"{API_PREFIX}{SERVICE_NAME}/status")
    def get_model_info(self) -> t.Dict[str, t.Any]:
        return {"model": "Logistic Regression", "status": "Trained"}


svc = StartService()
