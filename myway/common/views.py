#!/usr/bin/env python
#coding=utf-8

import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db
from myway.blog.models import Article
from .models import User
from .forms import LoginForm
from .login import login_user, logout_user

moduleid = 'common'
commonview = Blueprint(moduleid, __name__)


@commonview.route('/')
def layout():
    return redirect(url_for('blog.index'))

@commonview.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(next=request.args.get('next', ''))
    if form.is_submitted and form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        next = form.next.data
        user, authenticated =  User.authenticate(login, password)
        if user and authenticated:
            login_user(user, remember=True)
            flash('Log in successed!', 'success')
            if next:
                return redirect(next)
            return redirect('/blog/')
        flash('Username or password is wrong!', 'error')
    return render_template('common/login.html', form=form)

    
@commonview.route('/logout')
def logout():
    logout_user()
    flash('Log out successed!', 'success')
    return redirect('/blog/')
