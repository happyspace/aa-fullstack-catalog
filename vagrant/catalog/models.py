from sqlalchemy import Column, Integer, Unicode, BigInteger, DateTime
from sqlalchemy import UniqueConstraint, UnicodeText, ForeignKey
from sqlalchemy.orm import validates, relationship
import datetime
from database_setup import Base
from sqlalchemy.dialects.postgresql import JSON


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(Unicode(80), nullable=False)
    # Facebook users may not have signed up with an email.
    email = Column(Unicode(254), nullable=True)

    # URI for picture data
    picture = Column(Unicode(250))
    create_date = Column('create_date', DateTime,
                         default=datetime.datetime.now,
                         nullable=False)
    last_update = Column('last_update', DateTime,
                         onupdate=datetime.datetime.now,
                         nullable=False)
    items = relationship('Item')

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

    UniqueConstraint(name, name='category_name_unique')
    items = relationship('Item')

    def __init__(self,
                 name: str,
                 description: str):
        self.name = name,
        self.description = description


class Item(Base):
    __tablename__ = 'item'
    # synthetic key used to data relationships
    id = Column(BigInteger, primary_key=True)
    # natural key UUID used after encoding in URL displayed to clients.
    # RFC4122 - 36 characters - 32 hex digits and 4 dashes
    _uuid = Column(Unicode(36), nullable=False)

    name = Column(Unicode(200), nullable=False)
    description = Column(UnicodeText, nullable=False)
    create_date = Column('create_date', DateTime,
                         default=datetime.datetime.now,
                         nullable=False)
    last_update = Column('last_update', DateTime,
                         onupdate=datetime.datetime.now,
                         nullable=False)

    deleted_date = Column('deleted_date', DateTime,
                          nullable=True)
    owner_id = Column('owner_id', BigInteger, ForeignKey('user.id'))
    owner = relationship(User, back_populates="items")

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, back_populates="items")

    @property
    def uuid(self):
        """
        UUID is read only once set during creation.
        Returns :
            str: A string representation of the UUID.
        """
        return self._uuid

    @validates('name', 'description', 'owner', 'picture')
    def validate_not_deleted(self, key, value):
        """
        To preserve an item's history, items are not deleted
        but are marked as deleted. Once marked as deleted an item
        should not be updated in any way.

        """
        assert self.deleted_date is None
        return value

    # add uniqueness constraint since UUID method 4 allows a
    # tiny tiny chance of collision
    UniqueConstraint(_uuid, name='item_uuid_unique')

    def __init__(self,
                 uuid: str,
                 name: str,
                 description: str,
                 owner: User):
        self._uuid = uuid,
        self.name = name,
        self.description = description
        self.owner = owner
        self.owner_id = owner.id


class OaProvider(Base):
    __tablename__ = 'oa_provider'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(20), nullable=False)
    description = Column(Unicode(250))
    applications = relationship('Application')

    def __init__(self,
                 name: str,
                 description: str,
                 application_id: str):
        self.name = name,
        self.description = description,
        self.application_id = application_id

    UniqueConstraint(name, name='oa_provider_name_unique')


class Application(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    provider_id = Column('provider_id', Integer, ForeignKey('oa_provider.id'))
    provider = relationship(OaProvider, back_populates='applications')
    app_id = Column(Unicode(250), nullable=False)
    app_secret = Column(Unicode(250), nullable=False)
    json = Column(JSON, nullable=False)

    def __init__(self,
                 app_id: str,
                 app_secret: str,
                 json: str):
        self.app_id = app_id,
        self.app_secret = app_secret,
        self.json = json

    UniqueConstraint(provider_id, app_id, name='application_provider_app_unique')


class UserLogin(Base):
    __tablename__ = 'user_login'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship(User)
    oa_provider_id = Column(Integer, ForeignKey('oa_provider.id'))
    oa_provider = relationship(OaProvider)
    login_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    logout_date = Column(DateTime)

    def __init__(self,
                 user: User,
                 oa_provider: OaProvider):
        self.user = user,
        self.user_id = user.id,
        self.oa_provider = oa_provider,
        self.oa_provider_id = oa_provider.id






