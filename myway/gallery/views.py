#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db, navbar
from myway.gallery.models import Image

moduleid = 'gallery'
galleryview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)


@galleryview.route('/')
def index():
    LIMIT = 10
    key = request.args.get('key', '')
    query = Image.query
    if key:
        query = query.filter(db.or_(Image.source_name.ilike('%%%s%%' % key),
                                Image.title.ilike('%%%s%%' % key)))
    images = query.order_by(Image.id.desc()).offset(0).limit(LIMIT).all()
    return render_template('gallery/index.html', key=key, images=images)


@galleryview.route('/view/<int:id>')
def view(id):
    image = Image.query.get_or_404(id)
    return render_template('gallery/view.html', image=image)


@galleryview.route('/upload', methods=['GET', 'POST'])
def upload():
    from myway.gallery.forms import ImageForm
    form = ImageForm()

    if form.validate_on_submit():
        image = Image()
        image.save(form.image.data, form.tag.data, form.title.data)
        db.session.commit()
        flash(u'%s(%s) Uploaded!' % (image.source_name, image.title), 'success')
        return redirect(url_for('gallery.upload'))

    return render_template('gallery/upload.html', form=form)


@galleryview.route('/edit/<int:id>')
def edit(id):
    image = Image.query.get_or_404(id)
    title = request.args.get('title')
    flash('Title Changed!(from <%s> to <%s>)' % (image.title, title), 'success')
    image.title = title
    db.session.commit()
    return redirect('/gallery/')


@galleryview.route('/delete/<int:id>')
def delete(id):
    image = Image.query.get_or_404(id)
    image.delete()
    db.session.commit()
    flash(u'%s(%s) Deleted!' % (image.source_name, image.title), 'success')
    return redirect('/gallery/')


    
@galleryview.context_processor
def inject_navid():
    return dict(navid=moduleid)
    
navbar.add(moduleid, moduleid.title(), '/%s/' % moduleid)
