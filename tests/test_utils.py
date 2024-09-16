import pytest
import numpy as np
from app.utils import fetch_latest_data, prepare_data, predict_future_prices
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler  # Add this import
import tensorflow as tf

@pytest.mark.parametrize("ticker, sequence_length", [
    ("AAPL", 60),
    ("MSFT", 30),
    ("NFLX", 90),
    ("GOOGL", 45),
])
def test_fetch_latest_data(ticker, sequence_length):
    data = fetch_latest_data(ticker, sequence_length)
    assert isinstance(data, np.ndarray)
    assert len(data) == sequence_length

def test_prepare_data():
    data = np.random.rand(100)
    sequence_length = 60
    scaled_data, scaler = prepare_data(data, sequence_length)
    assert scaled_data.shape == (100, 1)
    assert scaled_data.min() >= 0 and scaled_data.max() <= 1

def test_predict_future_prices():
    # Create a dummy model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(60, 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')

    # Create dummy data
    last_sequence = np.random.rand(60, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(np.random.rand(100).reshape(-1, 1))
    days = 30

    future_prices = predict_future_prices(model, last_sequence, scaler, days)
    assert future_prices.shape == (days, 1)
    assert np.all(future_prices >= 0)  # Assuming stock prices are always non-negative

def test_model_prediction():
    # Load the actual model
    model_path = 'app/models/AAPL_model.h5'
    model = tf.keras.models.load_model(model_path)

    # Create dummy data
    last_sequence = np.random.rand(60, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(np.random.rand(100).reshape(-1, 1))
    days = 30

    future_prices = predict_future_prices(model, last_sequence, scaler, days)
    assert future_prices.shape == (days, 1)
    assert np.all(future_prices >= 0)  # Assuming stock prices are always non-negative