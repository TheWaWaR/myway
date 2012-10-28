#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db, navbar

moduleid = 'vps'
vpsview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

    
@vpsview.context_processor
def inject_navid():
    return dict(navid=moduleid)
    
navbar.add(moduleid, moduleid.title(), '/%s/' % moduleid)
