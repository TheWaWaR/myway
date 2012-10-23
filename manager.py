#!/usr/bin/env python
#coding=utf-8

import sys
from myway import create_app

def create_all():
    from myway.utils import db
    db.create_all()
    print 'DB created!'

func = {}
func['create_all'] = create_all

app = create_app('settings.py')
if __name__ == '__main__':
    print globals()
    if len(sys.argv) > 1:
        name = sys.argv[1]
        args = sys.argv[2:]
        apply(func[name], args)
    
    app.run(host='0.0.0.0', port=1989)
