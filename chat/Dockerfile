FROM python:3.11.6-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential ffmpeg \
  && pip install --no-cache-dir --upgrade pip

RUN apt-get install -y libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
