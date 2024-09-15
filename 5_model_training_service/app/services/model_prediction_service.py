import typing as t
import bentoml
import pandas as pd


@bentoml.service()
class ModelPredictionService():
    @bentoml.api()
    def predict(self) -> t.List[float]:
        data = [
            {
                "open": 10.0,
                "high": 15.0,
                "low": 9.0,
                "close": 14.0,
                "volume": 1000,
                "mid_price": 12.0,
                "volatility": 6.0,
                "price_increase": 1
            },
            {
                "open": 11.0,
                "high": 16.0,
                "low": 10.0,
                "close": 15.0,
                "volume": 1100,
                "mid_price": 13.0,
                "volatility": 6.0,
                "price_increase": 0
            }
        ]
        df = pd.DataFrame(data)
        X = df[['open', 'high', 'low', 'close',
                'volume', 'mid_price', 'volatility']]
        model = self.artifacts.model
        predictions = model.predict(X)
        return predictions.tolist()
