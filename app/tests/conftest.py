import os

import psycopg2
import pytest
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
	conn = psycopg2.connect(
		f"host=db dbname={os.environ.get('POSTGRES_DB')} user={os.environ.get('POSTGRES_USER')} password={os.environ.get('POSTGRES_PASSWORD')}")
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute(sql)
	conn.close()


@pytest.fixture(scope='session')
def django_db_setup():
	from django.conf import settings

	settings.DATABASES['default']['NAME'] = 'the_copied_db'

	run_sql('DROP DATABASE IF EXISTS the_copied_db')
	run_sql('CREATE DATABASE the_copied_db TEMPLATE app')

	yield

	for connection in connections.all():
		connection.close()

	run_sql('DROP DATABASE the_copied_db')
