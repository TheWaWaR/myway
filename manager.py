#!/usr/bin/env python
#coding=utf-8

import sys
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from myway import app

def create_db():
    from myway.utils import db
    db.create_all()
    print 'DB created!'

def rebuild_db():
    from myway.utils import db
    db.drop_all()
    db.create_all()
    print 'DB Rebuilt!'
    
func = {}
func['create_db'] = create_db
func['rebuild_db'] = rebuild_db

application = DispatcherMiddleware(app)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
        args = sys.argv[2:]
        apply(func[name], args)
    
    run_simple('0.0.0.0', 2012, application, use_reloader=True, use_debugger=True)
