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

    #Basci Auth
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME', 'john')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', 'matrix')

    #Passwords
    POSTGRES_MAIN_PASSWORD = os.environ.get('POSTGRES_MAIN_PASSWORD', NOT_FOUND)

    #Hosts
    #POSTGRES_MAIN_HOST = os.environ.get('POSTGRES_MAIN_HOST', 'postgresql-1601875415.sql.svc.cluster.local')
    #POSTGRES_REPLICATION_HOST= os.environ.get('POSTGRES_REPLICATION_HOST', 'postgresql-1601875415-read.sql.svc.cluster.local')		

    POSTGRES_MAIN_HOST = os.environ.get('POSTGRES_MAIN_HOST', '34.73.253.37')
    POSTGRES_REPLICATION_HOST= os.environ.get('POSTGRES_REPLICATION_HOST', '35.237.247.34')
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             f'postgresql+psycopg2://postgres:{POSTGRES_MAIN_PASSWORD}@{POSTGRES_MAIN_HOST}:5432/countries')

    SQLALCHEMY_DATABASE_REPLICA_URI = os.environ.get('SQLALCHEMY_DATABASE_REPLICA_URI',
                                             f'postgresql+psycopg2://postgres:{POSTGRES_MAIN_PASSWORD}@{POSTGRES_REPLICATION_HOST}:5432/countries')
    SQLALCHEMY_BINDS = {
        'replica':        SQLALCHEMY_DATABASE_REPLICA_URI
    }