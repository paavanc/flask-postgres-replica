"""Flask config class."""
import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SESSION_COOKIE_NAME = 'my_cookie'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'postgresql+psycopg2://test:test@0.0.0.0:5401/test')

    SQLALCHEMY_DATABASE_REPLICA_URI = os.environ.get('SQLALCHEMY_DATABASE_REPLICA_URI',
                                             'postgresql+psycopg2://test:test@0.0.0.0:5401/test')
    SQLALCHEMY_BINDS = {
        'replica':        SQLALCHEMY_DATABASE_REPLICA_URI
    }