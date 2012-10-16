#!/usr/bin/env python
#coding=utf-8

import os
from hashlib import md5
from datetime import datetime
from werkzeug import secure_filename

from flask import current_app
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from myway.utils import db
from myway.utils import rand

class Image(db.Model):
    __tablename__ = 'images'
    
    id          = Column(Integer, primary_key=True)
    source_name = Column(String(255))  # Source File name
    filename    = Column(String(255))  # hashlib.md5(source_name).hexdigest()
    title       = Column(String(1023)) # Also Description, Name
    thumb_id    = Column(Integer, ForeignKey('thumbs.id', ondelete='CASCADE'))
    create_at   = Column(DateTime, default=datetime.now)
    update_at   = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    thumb = db.relation('Thumb')

    @property
    def save_name(self):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        return os.path.join(upload_folder, self.filename)

        
    def save(self, file_data, title):
        source_name = secure_filename(file_data.filename)
        filename = '.'.join([md5(source_name).hexdigest() + str(rand.randint(0, 1000)),
                             source_name.split('.')[-1]])
        self.filename = filename
        
        thumb = Thumb()
        thumb.filename = 'thumb_' + filename
        
        file_data.save(self.save_name)
        from shutil import copyfile
        copyfile(self.save_name, thumb.save_name)
        
        db.session.add(thumb)
        self.source_name = source_name
        self.title = title
        self.thumb = thumb
        db.session.add(self)


    def delete(self):
        os.remove(self.thumb.save_name)
        os.remove(self.save_name)
        db.session.delete(self)
        
    @property
    def link(self):
        return os.path.join(current_app.config['UPLOAD_URI'], self.filename)
        

class Thumb(db.Model):
    __tablename__ = 'thumbs'

    id        = Column(Integer, primary_key=True)
    filename  = Column(String(255))
    create_at = Column(DateTime, default=datetime.now)
    
    @property
    def save_name(self):
        import os
        upload_folder = current_app.config['UPLOAD_FOLDER']
        return os.path.join(upload_folder, self.filename)
        
    @property
    def link(self):
        return os.path.join(current_app.config['UPLOAD_URI'], self.filename)
