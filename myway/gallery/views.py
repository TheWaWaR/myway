#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, \
    url_for, flash, current_app
from myway.common.login import current_user
from myway.utils import db, navbar
from myway.gallery.models import Image

moduleid = 'gallery'
galleryview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)


@galleryview.route('/')
def index():
    perpage = current_app.config['GALLERY_PERPAGE']
    page = request.args.get('page', 1, type=int)
    key = request.args.get('key', '')
    base_query = Image.query
    if current_user.is_anonymous():
        base_query = base_query.filter(Image.public==1)
    query = base_query
    if key:
        ikey = '%' + key + '%'
        query = query.filter(db.or_(Image.source_name.ilike(ikey),
                                    Image.title.ilike(ikey),
                                    Image.tag.ilike(ikey)))
    query = query.order_by(Image.create_at.desc())
    page_obj = query.paginate(page=page, per_page=perpage)
    page_url = lambda page : url_for('gallery.index', page=page)
    recents = base_query.order_by(Image.create_at.desc()).offset(0).limit(perpage)
    kwargs = {
        'key'     : key,
        'page_obj': page_obj,
        'page_url': page_url,
        'recents' : recents
    }
    return render_template('gallery/index.html', **kwargs)


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
        image.save(form.image.data, form.tag.data, form.title.data, form.is_public.data)
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
