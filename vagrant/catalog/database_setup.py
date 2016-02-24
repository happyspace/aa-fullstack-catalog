from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine("postgres://vagrant@localhost/catalog")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(254), nullable=False)
    picture = Column(String(250))


Base.metadata.create_all(engine)
