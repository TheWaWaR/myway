#!/usr/bin/env python
#coding=utf-8

from myway.utils import images
from wtforms.fields import TextField, TextAreaField, SelectField, FileField
from wtforms.validators import required
from flask_wtf import Form, file_allowed

class ImageForm(Form):
    image     = FileField(u'Image', validators=[required(message=u'Required!'),
                                           file_allowed(images, u'Image only!')])
    tag       = TextField(u'Tag', [required(message=u'Required!')])
    is_public = SelectField(u'Is public', choices=[(u'1', 'Public'), (u'0', 'Private')])
    title     = TextAreaField(u'Description')
