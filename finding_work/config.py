import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс параметров конфигурации"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hh_find.sqlite'
    SECRET_KEY = os.getenv('SECRET_KEY')
    KEY_REGISTER = os.getenv('KEY_REGISTER')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'ru'
