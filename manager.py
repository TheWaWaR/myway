#!/usr/bin/env python
#coding=utf-8

import sys
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from myway import app
from myway.common.models import User
from myway.blog.models import Category

def create_db():
    from myway.utils import db
    db.create_all()
    print 'DB created!'

def rebuild_db():
    from myway.utils import db
    db.drop_all()
    db.create_all()

    user = User()
    user.login = 'weet'
    user.password = 'hello123'
    db.session.add(user)
    category = Category()
    category.name = 'None'
    db.session.add(category)
    db.session.commit()
    print 'DB Rebuilt!'
    
func = {}
func['create_db'] = create_db
func['rebuild_db'] = rebuild_db


if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in func.keys():
            args = sys.argv[2:]
            apply(func[name], args)
            
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(2012)
    IOLoop.instance().start()
    # application = DispatcherMiddleware(app)
    # run_simple('0.0.0.0', 2012, application, use_reloader=True, use_debugger=False)
