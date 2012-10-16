#!/usr/bin/env python
#coding=utf-8

from myway.utils import images
from flask_wtf import Form, TextField, TextAreaField, FileField, required, file_allowed

class ImageForm(Form):
    image = FileField(u'图片', validators=[required(message=u'请选择一个图片文件'),
                                           file_allowed(images, u'只允许上传图片!')])
    title = TextAreaField(u'描述')
