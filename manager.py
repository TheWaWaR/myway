#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.insert(0, '.')

from myway.common.models import User
from myway.blog.models import Category

# ==============================================================================
#  Database
# ==============================================================================
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

# ==============================================================================
#  Application
# ==============================================================================
from myway import app
def run_product(app=app):
    pass

def run_debug(app=app):
    app.run(host='0.0.0.0', port=12012, debug=True)

# ==============================================================================
#  Function dict
# ==============================================================================
FUNCS = {
    'create_db'  : create_db,
    'rebuild_db' : rebuild_db,
    'product'    : run_product,
    'debug'      : run_debug
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in FUNCS.keys():
            args = sys.argv[2:]
            print 'Argument is correct!: ' + name
            apply(FUNCS[name], args)
        else:
            print '> Missing!: ' + name
    else:
        print 'Run under DEBUG'
        run_debug()
    print '========================================'
    print 'DONE!'
