#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db, navbar
from myway.common.login import current_user

moduleid = 'vps'
vpsview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

    
@vpsview.context_processor
def inject_navid():
    return dict(navid=moduleid)

def utf8(s):
    return unicode(s, encoding='utf-8')

@vpsview.route('/')
def index():
    if current_user.is_anonymous():
        return "Hey, It's is private!"
    return render_template('vps/index.html')


@vpsview.route('/exec', methods=['POST'])
def ajax_execute():
    if current_user.is_anonymous():
        return "Hey, It's is private!"
    command = request.form.get('command', 'None')
    from commands import getstatusoutput
    status, output = getstatusoutput(command)
    output = u'$ %s\n========================================\n%s' % (command, utf8(output))
    if status == 0:
        return output
    else:
        return '[Bad Command: %s]' % command
    
    
navbar.add(moduleid, moduleid.title(), '/%s/' % moduleid)
