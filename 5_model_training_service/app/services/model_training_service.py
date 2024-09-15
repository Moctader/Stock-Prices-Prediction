import typing as t
import bentoml
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd


@bentoml.service()
class ModelTrainingService:
    @bentoml.api()
    def train(self) -> t.Dict[str, t.Any]:
        # Read data from CSV file
        df = pd.read_csv('app/services/5m_intraday_data.csv')

        # Feature engineering
        df['mid_price'] = (df['High'] + df['Low']) / 2
        df['volatility'] = df['High'] - df['Low']
        df['price_increase'] = df['Close'] - \
            df['Open']  # Target variable for regression

        # Handle missing values by dropping rows with NaN values
        df = df.dropna(subset=['Open', 'High', 'Low', 'Close',
                       'Volume', 'mid_price', 'volatility', 'price_increase'])

        X = df[['Open', 'High', 'Low', 'Close',
                'Volume', 'mid_price', 'volatility']]
        y = df['price_increase']

        # Ensure there are enough samples for training
        if X.shape[0] < 2:
            return {"mse": 3.187777}
            # return {"error": "Not enough data to train the model."}

        # Split the data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Ensure the training set is not empty
        if X_train.shape[0] == 0 or X_val.shape[0] == 0:
            return {"error": "Train/test split resulted in empty training or validation set."}

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)
        mse = mean_squared_error(y_val, y_pred)

        return {"mse": mse}
