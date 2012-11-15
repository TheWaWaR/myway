#!/usr/bin/env python
#coding=utf-8

import os
from hashlib import md5
from datetime import datetime
from PIL import Image as PILImage

from werkzeug import secure_filename
from flask import current_app

from myway.utils import db
from myway.utils import rand

class Image(db.Model):
    __tablename__ = 'images'

    id          = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(200))  # Source File name
    filename    = db.Column(db.String(200))  # hashlib.md5(source_name).hexdigest()
    tag         = db.Column(db.String(100))  # Reference from the article
    title       = db.Column(db.String(200))  # Also Description, Name
    thumb_id    = db.Column(db.Integer, db.ForeignKey('thumbs.id', ondelete='CASCADE'))
    is_public   = db.Column(db.Integer(1), default=1)
    create_at   = db.Column(db.DateTime, default=datetime.now)
    update_at   = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    thumb = db.relation('Thumb')

    @property
    def path(self):
        upload_folder = current_app.config['UPLOADED_IMAGES_DEST']
        return os.path.join(upload_folder, self.filename)

        
    def save(self, file_data, tag, title, is_public):
        source_name = secure_filename(file_data.filename)
        filename = '.'.join([md5(source_name).hexdigest() + str(rand.randint(0, 1000)),
                             source_name.split('.')[-1]])
        self.filename = filename
        file_data.save(self.path)
        
        thumb = Thumb()
        thumb.filename = filename
        thumb.save(self.path)
        db.session.add(thumb)
        
        self.source_name = source_name
        self.tag = tag
        self.title = title
	self.is_public = is_public
        self.thumb = thumb
        db.session.add(self)


    def delete(self):
        os.remove(self.thumb.path)
        os.remove(self.path)
        db.session.delete(self)
        
    @property
    def link(self):
        return os.path.join(current_app.config['IMAGES_URI'], self.filename)
        

class Thumb(db.Model):
    __tablename__ = 'thumbs'

    id        = db.Column(db.Integer, primary_key=True)
    filename  = db.Column(db.String(255))
    create_at = db.Column(db.DateTime, default=datetime.now)
    
    @property
    def path(self):
        upload_folder = current_app.config['UPLOADED_THUMBS_DEST']
        return os.path.join(upload_folder, self.filename)

    def save(self, img_path):
        im = PILImage.open(img_path)
        iwidth, iheight = im.size
        max_width = current_app.config['THUMBS_MAX_WIDTH']
        if iwidth > max_width:
            iheight = iheight/(float(iwidth)/max_width)
            iwidth = max_width
        im.thumbnail((iwidth, iheight), PILImage.ANTIALIAS)
        im.save(self.path)
        
        
    @property
    def link(self):
        return os.path.join(current_app.config['THUMBS_URI'], self.filename)
