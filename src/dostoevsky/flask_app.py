from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dostoevsky import config
from dostoevsky import model
from dostoevsky import orm
from dostoevsky import repository

orm.start_mappers()
# TODO: Move db creation to a separate script
engine = create_engine(config.get_postgres_uri())
orm.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)
app = Flask(__name__)

# TODO: get all data
# TODO: all filters


@app.route("/data", methods=["GET"])
def data():
    session = get_session()
    session.execute(
        'INSERT INTO parts (name, part, year, "totalConvicted", "primaryLifeSentence") VALUES '
        "('Убийство', '105ч.1', '2010',  10056, 3),"
        "('Убийство с отягчающими', '105ч.2', '2010',  6001, 0),"
        "('Убийство матерью', '106', '2010',  5368, 1),"
        "('Убийство', '105ч.1', '2011',  4579, 0),"
        "('Убийство с отягчающими', '105ч.2', '2011',  8932, 4),"
        "('Убийство матерью', '106', '2011',  10689, 1)"
    )
    columns = ["totalConvicted", "primaryLifeSentence"]
    split = ["part", "year"]
    data = repository.SqlAlchemyRepository(session).get_data(columns)
    print(data)
    return "OK", 201
