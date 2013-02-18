#!/usr/bin/env python
#coding=utf-8

from flask import Flask, g, request, redirect, url_for, render_template
from flask.ext.uploads import configure_uploads
from myway.utils import db, images, navbar, login_mgr
from myway.common.login import current_user

from myway.common.views import commonview
from myway.blog.views import blogview
from myway.project.views import projectview
from myway.vps.views import vpsview
# from myway.gallery.views import galleryview
# from myway.mldonkey.views import mldonkeyview
# from myway.chat.views import chatview

def create_app(cfg):
    app = Flask(__name__)
    app.config.from_pyfile(cfg)

    # Register Blueprints
    blueprints = [commonview, blogview, projectview, vpsview]
    for bp in blueprints:
        app.register_blueprint(bp)

    # Init app
    db.init_app(app)
    login_mgr.init_app(app)
    db.app = app
    configure_uploads(app, (images, ))

    @app.context_processor
    def inject_vars():
        vars = {
            'islogin' : not current_user.is_anonymous()
        }
        return vars

    return app


app = create_app('settings.py')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('common/404.html'), 404


@app.before_request
def before_request():
    g.navbar = navbar

    if current_user.is_anonymous():
        endpoint = request.endpoint
        if endpoint and endpoint.split('.')[-1] in ('new', 'edit', 'delete', 'upload'):
            return redirect(url_for('common.login', next=request.url))


