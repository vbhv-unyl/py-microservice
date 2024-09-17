FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    pkg-config \
    libhdf5-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
