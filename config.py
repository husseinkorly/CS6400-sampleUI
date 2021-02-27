from os import environ
from dotenv import load_dotenv


# configuration class for all app config
class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret_string'

    # database settings
    DATABASE_HOST = ''
    DATABASE_USERNAME = ''
    DATABASE_PASSWORD = ''
    DATABASE_PORT = '5432'
    DATABASE_NAME = 'postgres'
