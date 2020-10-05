"""Flask config class."""
import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SESSION_COOKIE_NAME = 'my_cookie'
    NOT_FOUND = 'NOT_FOUND'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #
    DEBUG_MODE = os.environ.get('DEBUG_MODE', NOT_FOUND)

    #Basci Auth
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME', NOT_FOUND)
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', NOT_FOUND)

    #Passwords
    POSTGRES_MAIN_PASSWORD = os.environ.get('POSTGRES_MAIN_PASSWORD', NOT_FOUND)

    #Hosts
    POSTGRES_MAIN_HOST = os.environ.get('POSTGRES_MAIN_HOST', NOT_FOUND)
    POSTGRES_REPLICATION_HOST= os.environ.get('POSTGRES_REPLICATION_HOST', NOT_FOUND)

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             f'postgresql+psycopg2://postgres:{POSTGRES_MAIN_PASSWORD}@{POSTGRES_MAIN_HOST}:5432/countries')

    SQLALCHEMY_DATABASE_REPLICA_URI = os.environ.get('SQLALCHEMY_DATABASE_REPLICA_URI',
                                             f'postgresql+psycopg2://postgres:{POSTGRES_MAIN_PASSWORD}@{POSTGRES_REPLICATION_HOST}:5432/countries')
    SQLALCHEMY_BINDS = {
        'replica':        SQLALCHEMY_DATABASE_REPLICA_URI
    }
