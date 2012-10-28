#!/usr/bin/env python
#coding=utf-8

from flask_wtf import Form, TextField, PasswordField, HiddenField, required

class LoginForm(Form):
    login = TextField('Username', [required(message='Required')])
    password = PasswordField('Password', [required(message='Required')])
    next = HiddenField()
