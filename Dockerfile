FROM python:3.10-slim-buster

RUN mkdir -p /src
COPY src/ /src/
COPY pyproject.toml /src 
COPY tests/ /tests/

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=dostoevsky/flask_app.py 
ENV FLASK_DEBUG=1

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD flask run --host=0.0.0.0 --port=80

