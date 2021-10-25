import os

from .base import *  # noqa

SECRET_KEY = os.environ.get('SECRET_KEY')
