import time
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, close_all_sessions

from dostoevsky.adapters.orm import metadata, start_mappers
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
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield engine
    close_all_sessions()
    metadata.drop_all(engine)


@pytest.fixture
def postgres_session_factory(postgres_db):
    yield sessionmaker(bind=postgres_db)


@pytest.fixture
def session(postgres_session_factory):
    session_factory = postgres_session_factory()
    yield session_factory


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../src/dostoevsky/entrypoints/flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()


@pytest.fixture
def test_rows(session):
    session.execute(
        'INSERT INTO parts (name, part, year, "totalConvicted", "primaryLifeSentence") VALUES '
        "('Убийство', '105ч.1', '2010',  10056, 3),"
        "('Убийство с отягчающими', '105ч.2', '2010',  6001, 0),"
        "('Убийство матерью', '106', '2010',  5368, 1),"
        "('Убийство', '105ч.1', '2011',  4579, 0),"
        "('Убийство с отягчающими', '105ч.2', '2011',  8932, 4),"
        "('Убийство матерью', '106', '2011',  10689, 1)"
    )
