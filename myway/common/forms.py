#!/usr/bin/env python
#coding=utf-8

from wtforms.fields import TextField, PasswordField, HiddenField 
from wtforms.validators import required
from flask_wtf import Form

class LoginForm(Form):
    login = TextField('Username', [required(message='Required')])
    password = PasswordField('Password', [required(message='Required')])
    next = HiddenField()
