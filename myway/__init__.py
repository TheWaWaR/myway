#!/usr/bin/env python
#coding=utf-8

from flask import Flask
from flask.ext.uploads import configure_uploads
from myway.utils import db, images

from myway.common.views import commonview
from myway.gallery.views import galleryview
from myway.blog.views import blogview
from myway.project.views import projectview
from myway.mldonkey.views import mldonkeyview
from myway.chat.views import chatview
from myway.vps.views import vpsview

def create_app(cfg):
    app = Flask(__name__)
    app.config.from_pyfile(cfg)

    # Register Blueprints
    blueprints = [commonview, galleryview, blogview,
                  projectview, mldonkeyview, chatview, vpsview]
    for bp in blueprints:
        app.register_blueprint(bp)

    # Init app
    db.init_app(app)
    db.app = app
    configure_uploads(app, (images, ))
    
    return app

app = create_app('settings.py')
