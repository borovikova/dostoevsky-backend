from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dostoevsky import config
from dostoevsky.domain import model
from dostoevsky.adapters import orm, repository
from dostoevsky.service_layer import services

orm.start_mappers()
# TODO: Move db creation to a separate script
engine = create_engine(config.get_postgres_uri())
#orm.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)
app = Flask(__name__)

# TODO: get all data
# TODO: all filters


@app.route("/data", methods=["GET"])
def data():
    session = get_session()
    services.get_all(session)

    return "OK", 201
