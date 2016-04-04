from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine


engine = create_engine("postgres://vagrant@localhost/catalog")

# Default scoped_session uses thread local storage
# which will be fine here. For Flask use '_app_ctx_stack'
# to match Flask session and application context.
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()





