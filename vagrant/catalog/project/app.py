from flask import Flask, render_template, Response, request
from flask import _app_ctx_stack as stack
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from config.config import Config, DevelopmentConfig
from main.views import main


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

    @_app.teardown_appcontext
    def teardown(exception=None):
        if _app.db_session:
            _app.db_session.remove()

    # register blue prints
    _app.register_blueprint(main)
    return _app


if __name__ == '__main__':
    config = DevelopmentConfig()
    app = create_app(config)
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
