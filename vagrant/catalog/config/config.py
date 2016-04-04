"""
Organize config as classes as per the following
from the flask documentation:

    http://flask.pocoo.org/docs/0.10/config/#development-production

Flask configuration values can be found:

    http://flask.pocoo.org/docs/0.10/config/#builtin-configuration-values

Use to instantiate a configuration.:

    app.config.from_object('config.ProductionConfig')

"""


class Config(object):
    """
    Base configuration.
    """
    # Flask
    DEBUG = False
    TESTING = False
    # SQLAlchemy
    DATABASE_URI = 'postgres://vagrant@localhost/catalog'
    # WSGI
    HOST = '0.0.0.0'
    PORT = 5003
    KEY = 'super_secret_key'


class ProductionConfig(Config):
    """
    Production configuration
    """
    # add overrides here


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    # Flask
    DEBUG = True


class TestingConfig(Config):
    """
    Test configuration
    """
    #Flask
    TESTING = True


