#coding=utf-8

DEBUG = True

SECRET_KEY = 'How do you know the key???'
SESSION_COOKIE_NAME = 'myway'

IMAGE_EXTS = ('png', 'jpg', 'jpeg', 'gif', 'bmp')
IMAGE_EXTS_STR = '|'.join(['%s|%s' % (ext, ext.upper()) for ext in IMAGE_EXTS])
UPLOAD_URI = '/static/uploads/'

from myway.local_settings import ROOT
LOG_PATH = ROOT + 'log/'
UPLOAD_FOLDER = ROOT + 'myway/static/uploads/'
IMAGES_URI = UPLOAD_URI + 'images/'
THUMBS_URI = IMAGES_URI + 'thumbs/'
UPLOADED_IMAGES_DEST = UPLOAD_FOLDER + 'images/'
UPLOADED_THUMBS_DEST = UPLOADED_IMAGES_DEST + 'thumbs/'
THUMBS_MAX_WIDTH = 300

# SQLAlchemy
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 10

BLOG_PERPAGE = 5
GALLERY_PERPAGE = 8

from myway.local_settings import *
# SQLALCHEMY_DATABASE_URI = 'mysql://root:hello123@localhost/myway'
# ROOT = '/root/Projects/myway/
