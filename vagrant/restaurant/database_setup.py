import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


def fetch_restaurant(session, r_id):
    """

    :rtype : Restaurant
    """
    restaurant = None
    try:
        restaurant = session.query(Restaurant).filter(Restaurant.id == r_id).one()
    except (NoResultFound, MultipleResultsFound) as e:
        pass
    return restaurant


def fetch_restaurants(session):
    """

    :param session: sessionmaker
    """
    restaurants = (session.query(Restaurant).all())
    return restaurants


def update_restaurant(session, r_id, name):
    restaurant = fetch_restaurant(session, r_id)
    if restaurant:
        restaurant.name = name
        session.commit()
    return restaurant


def delete_restaurant(session, restaurant):
    if restaurant:
        session.delete(restaurant)
        session.commit()


def create_restaurant(session, name):
    new_restaurant = Restaurant(name=name)
    session.add(new_restaurant)
    session.commit()


if __name__ == "__main__":
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.create_all(engine)

    db_session = sessionmaker(bind=engine)





