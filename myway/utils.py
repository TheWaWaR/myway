#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from random import Random
from flask_sqlalchemy import SQLAlchemy
from flask.ext.uploads import UploadSet, IMAGES

db = SQLAlchemy()

images = UploadSet("images", IMAGES)
rand = Random(datetime.now())
