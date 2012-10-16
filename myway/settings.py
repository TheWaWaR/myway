#coding=utf-8

DEBUG = True

SECRET_KEY = 'How do you know the key???'
SESSION_COOKIE_NAME = 'myway'

IMAGE_EXTS = ('png', 'jpg', 'jpeg', 'gif', 'bmp')
IMAGE_EXTS_STR = '|'.join(['%s|%s' % (ext, ext.upper()) for ext in IMAGE_EXTS])
UPLOAD_URI = '/static/uploads/images'
UPLOAD_FOLDER = None

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = None
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 10

from myway.local_settings import *
