from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# select all puppies return in ascending order
def get_puppies(dbsession):
    print "get_puppies"
    puppies = session.query(Puppy).order_by(Puppy.name).all()
    for puppy in puppies:
        print puppy.name, puppy.gender, puppy.dateOfBirth


if __name__ == '__main__':
    get_puppies(session)