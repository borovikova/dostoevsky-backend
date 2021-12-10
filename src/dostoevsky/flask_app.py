from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dostoevsky import config
from dostoevsky import model
from dostoevsky import orm
from dostoevsky import repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

# TODO: get all data
# TODO: all filters


@app.route("/data", methods=["GET"])
def data():
    session = get_session()
    columns = ["totalConvicted", "primaryLifeSentence"]
    split = ["part", "year"]
    data = repository.SqlAlchemyRepository(session).get_data(columns)
    print(data)
    return "OK", 201
