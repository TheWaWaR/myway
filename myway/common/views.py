#!/usr/bin/env python
#coding=utf-8

import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db
from myway.blog.models import Article
from .models import User

commonview = Blueprint('common', __name__)


@commonview.route('/')
def layout():
    return render_template('layout.html')

@commonview.route('/test-md')
def save_md():
    import re
    from flask import current_app
    md_dir = os.path.join(current_app.root_path, 'static/markdown')
    md_files = os.listdir(md_dir)
    meta_patt = '^- +(\w+) *: *(.+)$'
    for file_name in md_files:
        f =  open(os.path.join(md_dir, file_name), 'r')
        article = Article()

        content = ''
        recording = True
        for line in f.readlines():
            if line.startswith('---'):
                recording = False
            elif recording:
                name, value = re.search(meta_patt, line)
                setattr(article, name, value)
            else:
                content += line
                
    return 'OK'
