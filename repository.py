from sqlalchemy import insert
from orm import parameters


class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, rows):
        self.session.execute(
            insert(parameters),
            [
                {
                    "name": parameter.name,
                    "part": parameter.part,
                    "parameter": parameter.parameter,
                    "value": parameter.value,
                    "year": parameter.year,
                    "category": parameter.category
                }
                for parameter in rows
            ],
        )
