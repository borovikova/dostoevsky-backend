from typing import Dict, List
from sqlalchemy.orm import load_only, Query
from sqlalchemy import insert, func

from dostoevsky.orm import parts
from dostoevsky.model import Part


def filter_query(q: Query, filters: Dict[str, list]):
    years_ = filters.get("year")
    if years_:
        q = q.filter(parts.c.year.in_(years_))

    parts_ = filters.get("part")
    if parts_:
        q = q.filter(parts.c.part.in_(parts_))

    return q


class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, rows):
        self.session.execute(insert(parts), [part.__dict__ for part in rows])

    def get_data(
        self,
        columns: List[str],
        filters: Dict[str, list] = None,
        split: List[str] = None,
    ):
        q = self.session.query()

        if filters:
            q = filter_query(q, filters)

        if split:
            groupby = [getattr(parts.c, col).label(col) for col in split]

            if "part" in split:
                q = q.add_columns(parts.c.name, parts.c.category)
                split.extend(["name", "category"])

            q = q.add_columns(*groupby).group_by(*split)

        aggregate = [
            func.sum(getattr(parts.c, col).label(col + "_")) for col in columns
        ]
        q = q.add_columns(*aggregate)

        return q.all()
