#!/usr/bin/env python
#coding=utf-8

from flask import Flask
from flask.ext.uploads import configure_uploads
from myway.gallery.views import galleryview
from myway.utils import db, images

def create_app(cfg):
    app = Flask(__name__)
    app.config.from_pyfile(cfg)

    # Register Blueprints
    blueprints = [galleryview]
    for bp in blueprints:
        app.register_blueprint(bp)

    # Init app
    db.init_app(app)
    db.app = app
    configure_uploads(app, (images, ))
    
    return app
