from typing import Dict, List
from sqlalchemy.orm import load_only, Query
from sqlalchemy import insert, func
from orm import parts
from model import Part


def filter_query(q: Query, filters: Dict[str, list]):
    years = filters["year"]
    if years:
        q = q.filter(Part.year.in_(years))

    parts = filters["part"]
    if parts:
        q = q.filter(Part.part.in_(parts))

    return q


class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, rows):
        self.session.execute(
            insert(parts),
            [part.__dict__ for part in rows],
        )

    def get_data(
        self,
        columns: List[str],
        filters: Dict[str, list] = None,
        split: List[str] = None,
    ):
        q = self.session.query()

        if "part" in split:
            q = q.add_columns(Part.name, Part.category)

        if filters:
            q = filter_query(q, filters)

        groupby = [getattr(Part, col).label(col) for col in split]
        q = q.add_columns(*groupby).group_by(*split)

        aggregate = [func.sum(getattr(Part, col).label(col + "_")) for col in columns]
        q = q.add_columns(*aggregate)

        return q.all()
