import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from app.utils.config import DATA_PATH


def load_data():
    data = pd.read_csv(DATA_PATH)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Previous_Close'] = data['Close'].shift(1)
    data = data.dropna()
    return data


def get_data_head():
    data = load_data()
    return data.head()


def predict_stock_prices():
    data = load_data()
    X = data[['Previous_Close']]
    y = data['Close']
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse, y_pred
