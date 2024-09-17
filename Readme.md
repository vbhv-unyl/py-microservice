# Stock Prediction API 📈🤖

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.5.0-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

A powerful and easy-to-use API for predicting stock prices using machine learning models. This project leverages Flask, TensorFlow, and yfinance to provide accurate stock price predictions for multiple tickers.

## 🌟 Features

- 🔮 Predict stock prices for multiple tickers (AAPL, MSFT, NFLX, GOOGL)
- ⏱️ Flexible prediction durations (days, months, years)
- 🔄 Real-time data fetching using yfinance
- 🐳 Docker support for easy deployment
- 🧪 Comprehensive test suite
- 🔍 Health check endpoint for monitoring

## 🛠️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stock_prediction_api.git
   cd stock_prediction_api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Start the Flask server:
   ```
   python run.py
   ```

2. The API will be available at `http://localhost:5000`

### API Endpoints

- **Health Check**: `GET /health`
- **Predict Stock Price**: `POST /predict`

  Example request body:
  ```json
  {
    "ticker": "AAPL",
    "duration": 30,
    "unit": "days"
  }
  ```

## 🐳 Docker Support

1. Build the Docker image:
   ```
   docker build -t stock-prediction-api .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 stock-prediction-api
   ```

## 🧪 Running Tests

Execute the test suite using pytest:

```
python -m pytest tests
```

## 📁 Project Structure

```
stock_prediction_api/
├── app/
│   ├── models/
│   │   └── [pre-trained model files]
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── .dockerignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── run.py
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/stock_prediction_api/issues).

Made with ❤️ by Vaibhav and Devashish