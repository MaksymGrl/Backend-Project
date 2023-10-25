FROM python:3.10.6-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app

CMD flask --app module run -h 0.0.0.0 -p $PORT