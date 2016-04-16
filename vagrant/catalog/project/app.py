from flask import Flask, render_template, Response, request, g
from flask import _app_ctx_stack as stack
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from config.config import Config, DevelopmentConfig
from main.views import main
from types import FunctionType
from enum import Enum


class StrEnum(str, Enum):
    """Enum where members are also (and must be) strings.

    String enumeration members are comparable to the string representation.
    Providers.google == 'google'
    """
    def __str__(self):
        return self.value


class Providers(StrEnum):
    """
    An Enumeration of supported providers.
    """
    facebook = 'facebook'
    google = 'google'


class ProviderDisconnect:
    """
    A mapping between a provider and Oauth API for disconnect.
    """
    disconnect = {}

    @classmethod
    def set_disconnect(cls, provider: StrEnum, func: FunctionType):
        cls.disconnect[provider] = func


class SessionFields(StrEnum):
    """
    An Enumeration representing all fields store in a user's session.
    """
    username = 'username'
    picture = 'picture'
    email = 'email'
    is_logged_in = 'is_logged_in'
    access_token = 'access_token'
    credentials = 'credentials'
    provider = 'provider'
    user_provider_id = 'user_provider_id'
    user_id = 'user_id'


def create_app(config_object: Config) -> Flask:
    """
    Create our application using the factory pattern.
    Code based on example flask documentation.
    http://flask.pocoo.org/docs/0.10/patterns/appfactories/
    and the following blog.
    http://piotr.banaszkiewicz.org/blog/2014/02/22/how-to-bite-flask-sqlalchemy-and-pytest-all-at-once/

    Args:
        config_object (config):

    Returns:
        Flask: a constructed flask application.

    """
    _app = Flask(__name__)
    _app.config.from_object(config_object)
    _app.secret_key = config_object.KEY
    # set up SQLAlchemy and session manager.
    engine = create_engine(config_object.DATABASE_URI)
    # Create a scoped session based on Flask's
    # use '_app_ctx_stack' session and application context.
    # engine = create_engine(config_object.DATABASE_URI)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine),
                                scopefunc=stack)

    _app.engine = engine
    _app.db_session = db_session

    with app.app_context():
        g.SessionFields = SessionFields

    @_app.teardown_appcontext
    def teardown(exception=None):
        """
        Teardown appcontext. Remove database session.
        Args:
            exception:
        """
        if _app.db_session:
            _app.db_session.remove()

    # register blue prints
    _app.register_blueprint(main)
    return _app


if __name__ == '__main__':
    config = DevelopmentConfig()
    app = create_app(config)
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
