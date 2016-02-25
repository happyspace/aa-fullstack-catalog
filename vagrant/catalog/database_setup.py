from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

engine = create_engine("postgres://vagrant@localhost/catalog")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(Unicode(80), nullable=False)
    email = Column(Unicode(254), nullable=False)
    picture = Column(Unicode(250))
    create_date = Column('create_date', DateTime, default=datetime.datetime.now, nullable=False)
    last_update = Column('last_update', DateTime, default=datetime.datetime.now, nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    description = Column(Unicode(200))


Base.metadata.create_all(engine)
