import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-big-old-secret'
	DATABASE_URI = 'sqlite://:memory:'