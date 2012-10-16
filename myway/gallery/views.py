#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db
from myway.gallery.models import Image

galleryview = Blueprint('gallery', __name__)


@galleryview.route('/')
def layout():
    return render_template('layout.html')

@galleryview.route('/gallery/')
def index():
    GALLERY_LEN = 10
    key = request.args.get('key', '')
    query = Image.query
    if key:
        query = query.filter(db.or_(Image.source_name.ilike('%%%s%%' % key),
                                Image.title.ilike('%%%s%%' % key)))
    images = query.order_by(Image.id.desc()).offset(0).limit(GALLERY_LEN).all()
    return render_template('gallery/index.html', key=key, images=images)


@galleryview.route('/gallery/view/<int:id>')
def view(id):
    image = Image.query.get_or_404(id)
    return render_template('gallery/view.html', image=image)


@galleryview.route('/gallery/upload', methods=['GET', 'POST'])
def upload():
    from myway.gallery.forms import ImageForm
    form = ImageForm()

    if form.validate_on_submit():
        image = Image()
        image.save(form.image.data, form.title.data)
        db.session.commit()
        flash(u'%s(%s) Uploaded!' % (image.source_name, image.title), 'success')
        return redirect(url_for('gallery.upload'))

    return render_template('gallery/upload.html', form=form)


@galleryview.route('/gallery/edit/<int:id>')
def edit(id):
    image = Image.query.get_or_404(id)
    title = request.args.get('title')
    flash('Title Changed!(from <%s> to <%s>)' % (image.title, title), 'success')
    image.title = title
    db.session.commit()
    return redirect('/gallery/')


@galleryview.route('/gallery/delete/<int:id>')
def delete(id):
    image = Image.query.get_or_404(id)
    image.delete()
    db.session.commit()
    flash(u'%s(%s) Deleted!' % (image.source_name, image.title), 'success')
    return redirect('/gallery/')



