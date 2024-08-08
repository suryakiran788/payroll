from os import getenv


class Config:
    SQLALCHEMY_DATABASE_URI = str(getenv('DATABASE_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
