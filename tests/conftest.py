import time
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, close_all_sessions

from dostoevsky.orm import metadata, start_mappers
from dostoevsky import config


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture()
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def postgres_session_factory(postgres_db):
    yield sessionmaker(bind=postgres_db)


@pytest.fixture
def session(postgres_session_factory):
    session_factory = postgres_session_factory()
    yield session_factory
    close_all_sessions()


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../src/dostoevsky/flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
