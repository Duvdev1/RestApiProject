from configparser import ConfigParser

from db_customer_repo import DbRepo
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# user-name: postgres
# password: admin
# database: customer_db


config = ConfigParser()
config.read("config3.conf")
connection_string = config["db"]["connection_string"]

Base = declarative_base()

engine = create_engine(connection_string, echo=True)

Session = sessionmaker()

local_session = Session(bind=engine)

db_repo = DbRepo(local_session)


def create_all_entities():
    Base.metadata.create_all(engine)
