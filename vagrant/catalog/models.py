from sqlalchemy import Column, Integer, String, Unicode, BigInteger, DateTime
import datetime
from database_setup import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(Unicode(80), nullable=False)
    email = Column(Unicode(254), nullable=False)
    picture = Column(Unicode(250))
    create_date = Column('create_date', DateTime, default=datetime.datetime.now, nullable=False)
    last_update = Column('last_update', DateTime, default=datetime.datetime.now, nullable=False)

    def __init__(self,
                 name: str,
                 email: str,
                 picture: str=None):
        self.name = name
        self.email = email
        self.picture = picture


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    description = Column(Unicode(200))

    def __init__(self,
                 name: str,
                 description: str):
        self.name = name,
        self.description = description
