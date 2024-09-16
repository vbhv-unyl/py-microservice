import pytest
from app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("ticker, duration, unit", [
    ("AAPL", 30, "days"),
    ("MSFT", 2, "months"),
    ("NFLX", 1, "years"),
    ("GOOGL", 7, "days"),
])
def test_predict_stock_price(client, ticker, duration, unit):
    response = client.post("/predict", json={
        "ticker": ticker,
        "duration": duration,
        "unit": unit
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["ticker"] == ticker
    assert data["duration"] == duration
    assert data["unit"] == unit
    assert isinstance(data["prediction"], float)

def test_predict_stock_price_invalid_ticker(client):
    response = client.post("/predict", json={
        "ticker": "INVALID",
        "duration": 30,
        "unit": "days"
    })
    assert response.status_code == 400
    assert "Model not available for this ticker" in json.loads(response.data)["error"]

def test_predict_stock_price_invalid_unit(client):
    response = client.post("/predict", json={
        "ticker": "AAPL",
        "duration": 30,
        "unit": "invalid"
    })
    assert response.status_code == 400
    assert "Invalid unit" in json.loads(response.data)["error"]