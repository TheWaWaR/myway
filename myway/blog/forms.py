#!/usr/bin/env python
#coding=utf-8

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import Form, TextField, TextAreaField, SelectField, required
from .models import Category

class ArticleForm(Form):
    title = TextField(u'Title', [required(message='Required')])
    category = QuerySelectField(u'Category', query_factory=lambda: Category.query, get_label='name')
    status = SelectField(u'Status', choices=[('1', 'Draft'), ('2', 'Pending Review'), ('3', 'Published'), ('4', 'Deleted')], default='1')
    visibility = SelectField(u'Visibility', choices=[('1', 'Public'), ('2', 'Password protected'), ('3', 'Private')], default='1')
    md_content = TextAreaField(u'')

