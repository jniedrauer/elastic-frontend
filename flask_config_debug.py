import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
SECRET_KEY = 'DONOTUSEINPRODUCTION'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

del os
