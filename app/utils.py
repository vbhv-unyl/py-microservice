import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

def fetch_latest_data(ticker, sequence_length):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=sequence_length * 2)  # Fetch extra data to ensure we have enough
    df = yf.download(ticker, start=start_date, end=end_date)
    return df['Close'].values[-sequence_length:]

def prepare_data(data, sequence_length):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    return scaled_data, scaler

def predict_future_prices(model, last_sequence, scaler, days):
    future_predictions = []
    current_sequence = last_sequence.copy()
    
    for _ in range(days):
        next_day_prediction = model.predict(np.array([current_sequence]))
        future_predictions.append(next_day_prediction[0, 0])
        current_sequence = np.roll(current_sequence, -1)
        current_sequence[-1] = next_day_prediction
    
    future_predictions = np.array(future_predictions).reshape(-1, 1)
    future_prices = scaler.inverse_transform(future_predictions)
    
    # Ensure all predictions are non-negative
    future_prices = np.maximum(future_prices, 0)
    
    return future_prices