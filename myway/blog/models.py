#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from myway.utils import db, md


class Article(db.Model):
    """ 文章 """
    __tablename__ = 'articles'
    
    id          = db.Column(db.Integer, primary_key=True)
    author_id   = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    title       = db.Column(db.String(200))
    status      = db.Column(db.Integer) # 1. Draft, 2. Pending Review, 3. Published, 4. Deleted,
    visibility  = db.Column(db.Integer) # 1. Public, 2. Password protected, 3. Private
    password    = db.Column(db.String(200))
    summary     = db.Column(db.Text)
    has_more    = db.Column(db.Boolean)
    content     = db.Column(db.Text)
    create_at   = db.Column(db.DateTime, default=datetime.now)
    update_at   = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    md_name        = db.Column(db.String(200))
    md_content     = db.Column(db.Text)
    md_last_modify = db.Column(db.DateTime, onupdate=datetime.now)
    
    author   = db.relationship('User')
    category = db.relationship('Category')

    def refresh(self):
        self.content = md.render(self.md_content)
        
        paragraphs = self.content.split('</p>')
        if not paragraphs[-1].strip(): paragraphs = paragraphs[:-1]
        plen = len(paragraphs)
        idx = length = 0
        for i in range(plen):
            length += len(paragraphs[i])
            idx = i
            if i >= 3 or length > 360 or \
               (i < plen-1 and length+len(paragraphs[i+1]) > 480):
                break
        self.has_more = True if idx < plen-1 else False
        self.summary = '</p>'.join(paragraphs[:idx+1]) + '</p>'

        
class Category(db.Model):
    """ 文章分类 """
    __tablename__ = 'categories'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100))
    descr      = db.Column(db.String(500))
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
