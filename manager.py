#!/usr/bin/env python
#coding=utf-8

from myway import create_app
from myway.utils import db

app = create_app('settings.py')

if __name__ == '__main__':
    # db.create_all()
    app.run(host='0.0.0.0', port=1989)
