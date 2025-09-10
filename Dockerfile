FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
 && pip install --only-binary=:all: -r requirements.txt

COPY . /app

CMD ["python", "src/app.py", "--nearest-demo", "--buffer", "75", "--output", "output.geojson"]
