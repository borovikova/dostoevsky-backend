import dataclasses
from typing import List
from dostoevsky.adapters import repository
from dostoevsky.domain.model import Part


def get_all(session, columns: List[str] = None):
    if not columns:
        columns = [field.name for field in dataclasses.fields(Part) if field.name not in ['name', 'part', 'category', 'year']]
        print(columns)
    return repository.SqlAlchemyRepository(session).get_data(columns)
