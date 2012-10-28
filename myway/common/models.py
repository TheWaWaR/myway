#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from myway.utils import db
from .login import UserMixin

class User(db.Model, UserMixin):
    """ 用户 """
    __tablename__ = 'users'
    
    id         = db.Column(db.Integer, primary_key=True)
    login      = db.Column(db.String(100))
    name       = db.Column(db.String(100))
    password   = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)

    def check_passwd(self, passwd):
        return self.password == passwd

    @classmethod
    def authenticate(clazz, login, passwd):
        user = clazz.query.filter(User.login==login).first()
        if user:
            authenticated = user.check_passwd(passwd)
        else:
            authenticated = False

        return user, authenticated
