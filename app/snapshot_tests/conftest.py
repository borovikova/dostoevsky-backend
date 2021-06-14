import pytest
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('fill_db')
        call_command('fill_db', file='part/data/2020.pkl')


# @pytest.fixture(scope='session')
# def django_db_setup():
# 	"""Avoid creating/setting up the test database"""
# 	pass
#
#
# @pytest.fixture
# def db_access_without_rollback_and_truncate(request, django_db_setup, django_db_blocker):
# 	django_db_blocker.unblock()
# 	request.addfinalizer(django_db_blocker.restore)
