import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class MenuItem(Base):
    __table__ = Table('menu_item', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(80), nullable=False),
                      Column('course', String(250)),
                      Column('description', String(250)),
                      Column('price', String(8)),
                      Column('restaurant_id', Integer, ForeignKey('restaurant.id')))

    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)