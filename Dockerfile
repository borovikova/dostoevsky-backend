FROM python:3.10-slim-buster

RUN mkdir -p /app
WORKDIR /app
COPY pyproject.toml /app 

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY src/ /app/src/
COPY tests/ /app/tests/

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=src/dostoevsky/entrypoints/flask_app.py 
ENV FLASK_DEBUG=1


CMD flask run --host=0.0.0.0 --port=80

