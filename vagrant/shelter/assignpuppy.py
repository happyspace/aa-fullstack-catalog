from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
import random

from puppies import Base, Shelter, Puppy

from puppypopulator import count_puppies, CreateRandomAge, CreateRandomWeight, puppy_images


GENDER = ('M', 'F')
GENDER_MAP = {'M': 'male', 'F': 'female'}


def assign_puppy(session):
    while True:
        name = prompt_puppy_name()
        g = gender()
        # get a shelter
        shelter = None
        while not shelter:
            sid = prompt_shelter_id()
            shelter = fetch_shelter(session, sid)
        # compare max to current number of puppies
        cp = count_puppies(session, shelter)
        print shelter.name + " " + str(shelter.maximum_capacity) + " " + str(cp)

        if cp < shelter.maximum_capacity:
            create_puppy(shelter, session, name, g)
        else:
            print shelter.name + " has maximum number of puppies " + str(shelter.maximum_capacity)
            shelter = fetch_next_best_shelter(session, shelter)
            if shelter:
                create_puppy(shelter, session, name, g)
            else:
                print "All shelters are full. Please open a new shelter."


def create_puppy(shelter, session, name, puppy_gender):
    new_puppy = Puppy(name=name, gender=GENDER_MAP[puppy_gender], dateOfBirth=CreateRandomAge(),
                      picture=random.choice(puppy_images),
                      shelter_id=shelter.id, weight=CreateRandomWeight())
    session.add(new_puppy)
    session.commit()


def prompt_puppy_name():
    pn = None
    while True:
        # noinspection PyBroadException
        try:
            pn = raw_input("Enter puppies name: ")
        except:
            pass
        if pn:
            break
    return pn


def prompt_shelter_id():
    sid = None
    while True:
        # noinspection PyBroadException
        try:
            sid = int(raw_input("Enter shelter ID: "))
        except:
            pass
        if sid:
            break
    return sid


def gender():
    g = None
    while True:
        # noinspection PyBroadException
        try:
            g = raw_input("Enter gender F or M: ")
        except:
            pass
        if g in GENDER:
            break
        else:
            g = None
    return g


def fetch_shelter(session, shelter_id):
    shelter = None
    # noinspection PyBroadException
    try:
        shelter = (session.query(Shelter).filter(Shelter.id == shelter_id).one())
    except:
        pass
    return shelter


def fetch_next_best_shelter(session, shelter):
    # get all the shelters except the
    shelters = (session.query(Shelter).all())

    # get the current number of puppies in each shelter

    # set on the entities

    # create a hybrid

    return shelters[0]


if __name__ == "__main__":
    engine = create_engine('sqlite:///puppyshelter.db', echo=True)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    _session = DBSession()

    # _shelter = fetch_shelter(_session, 1)
    # _cp = count_puppies(_session, _shelter)

    assign_puppy(_session)
