#!/usr/bin/env python
#coding=utf-8

import sys
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

if __name__ == '__main__':
    # print globals()
    if len(sys.argv) > 1:
        name = sys.argv[1]
        args = sys.argv[2:]
        apply(func[name], args)
    
    app.run(host='0.0.0.0', port=1989)
