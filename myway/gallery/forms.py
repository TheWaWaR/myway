#!/usr/bin/env python
#coding=utf-8

from myway.utils import images
from flask_wtf import Form, TextField, TextAreaField, FileField, required, file_allowed

class ImageForm(Form):
    image = FileField(u'Image', validators=[required(message=u'Required!'),
                                           file_allowed(images, u'Image only!')])
    tag   = TextField(u'Tag', [required(message=u'Required!')])
    title = TextAreaField(u'Description')
