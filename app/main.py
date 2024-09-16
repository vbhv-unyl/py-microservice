from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import os
import psutil
from app.utils import fetch_latest_data, prepare_data, predict_future_prices

main = Blueprint('main', __name__)

# Load pre-trained models
models = {}
tickers = ['AAPL', 'MSFT', 'NFLX', 'GOOGL']
for ticker in tickers:
    model_path = f'app/models/{ticker}_model.h5'
    if os.path.exists(model_path):
        models[ticker] = load_model(model_path)
    else:
        print(f"Model for {ticker} not found.")

@main.route('/health', methods=['GET'])
def health_check():
    try:
        # Try to make a prediction with dummy data
        dummy_ticker = 'AAPL'
        dummy_data = fetch_latest_data(dummy_ticker, 60)
        scaled_data, scaler = prepare_data(dummy_data, 60)
        future_prices = predict_future_prices(models[dummy_ticker], scaled_data, scaler, 1)
        model_status = f"operational (test prediction: {future_prices[-1][0]:.2f})"
    except Exception as e:
        model_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy",
        "message": "The service is up and running",
        "model_status": model_status,
        "memory_usage": psutil.virtual_memory().percent
    }), 200

@main.route('/predict', methods=['POST'])
def predict_stock_price():
    data = request.json
    ticker = data.get('ticker')
    duration = data.get('duration')
    unit = data.get('unit')

    if ticker not in models:
        return jsonify({"error": "Model not available for this ticker"}), 400
    
    if unit not in ['days', 'months', 'years']:
        return jsonify({"error": "Invalid unit. Use 'days', 'months', or 'years'"}), 400
    
    model = models[ticker]
    sequence_length = 60  # Assuming all models use the same sequence length
    
    # Convert duration to days
    if unit == 'months':
        days = duration * 30
    elif unit == 'years':
        days = duration * 365
    else:
        days = duration
    
    latest_data = fetch_latest_data(ticker, sequence_length)
    scaled_data, scaler = prepare_data(latest_data, sequence_length)
    
    future_prices = predict_future_prices(model, scaled_data, scaler, days)
    
    return jsonify({
        "ticker": ticker,
        "prediction": float(future_prices[-1][0]),
        "duration": duration,
        "unit": unit
    })