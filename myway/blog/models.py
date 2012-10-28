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
    content     = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.now)
    updated_at  = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    md_name        = db.Column(db.String(200))
    md_content     = db.Column(db.Text)
    md_last_modify = db.Column(db.DateTime, onupdate=datetime.now)
    
    author   = db.relationship('User')
    category = db.relationship('Category')

    def refresh(self):
        self.content = md.render(self.md_content)
        

class Category(db.Model):
    """ 文章分类 """
    __tablename__ = 'categories'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100))
    descr      = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
