from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

import model

metadata = MetaData()

parameters = Table(
    "parameters",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("parameter", String(255), nullable=False),
    Column("value", Integer, nullable=False),
    Column("year", String(4), nullable=False),
    Column("part", String(20), nullable=False),
    Column("name", String(255), nullable=False),
    Column("category", String(255), default="", nullable=False),
)


def start_mappers():
    parameters_mapper = mapper(model.Parameter, parameters)


# https://stackoverflow.com/questions/2089661/sqlalchemy-column-to-row-transformation-and-vice-versa-is-it-possible
# https://docs.sqlalchemy.org/en/14/orm/extensions/associationproxy.html?highlight=association%20proxy