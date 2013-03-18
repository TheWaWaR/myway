#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, redirect, url_for, \
    flash, request, current_app, abort
from myway.utils import db, navbar
from myway.common.login import current_user

from .models import Article
from .forms import ArticleForm

moduleid = 'blog'
blogview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

@blogview.route('/')
@blogview.route('/page/<int:page>')
def index(page=1):
    perpage = current_app.config['BLOG_PERPAGE']
    key = request.args.get('key', '')

    base_query = Article.query
    if current_user.is_anonymous():
        base_query = base_query.filter(db.and_(Article.status==3, Article.visibility < 2))
    base_query = base_query.order_by(Article.create_at.desc())

    query = base_query
    if key:
        ikey = '%' + key + '%'
        query = query.filter(db.or_(Article.title.ilike(ikey), Article.md_content.ilike(ikey)))

    page_obj = query.paginate(page=page, per_page=perpage)
    page_url = lambda page: url_for('blog.index', page=page)
    recents = base_query.offset(0).limit(perpage)
    kwargs = {
        'key'      : key,
        'page_obj' : page_obj,
        'page_url' : page_url,
        'recents'  : recents
    }
    return render_template('blog/index.html', **kwargs)


@blogview.route('/<int:id>')
def single(id):
    query = Article.query.filter_by(id=id)
    if current_user.is_anonymous():
        query = query.filter(db.and_(Article.status==3,
                                     Article.visibility<3))
    article = query.first()
    if not article: abort(404)
    return render_template('blog/single.html', article=article)


@blogview.route('/new', methods=['GET', 'POST'])
def new():
    form = ArticleForm()
    if form.is_submitted and form.validate_on_submit():
        article = Article()
        form.populate_obj(article)
        article.refresh()
        db.session.add(article)
        db.session.commit()
        flash('New article added!', 'success')
        return redirect(url_for('blog.edit', id=article.id))

    kwargs = {
        'form'   : form,
        'action' : url_for('blog.new'),
        'title'  : u'New Article'
    }
    return render_template('blog/new-edit.html', **kwargs)



@blogview.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)
    if form.is_submitted and form.validate_on_submit():
        form.populate_obj(article)
        article.refresh()
        db.session.commit()
        flash('Updated!', 'success')
        return redirect(url_for('blog.edit', id=article.id))
    form.process(obj=article)

    kwargs = {
        'form'      : form,
        'action'    : url_for('blog.edit', id=id),
        'view_link' : url_for('blog.single', id=id),
        'title'     : u'Edit: %s' % article.title
    }
    return render_template('blog/new-edit.html', **kwargs)




@blogview.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash(u'Article: <%s> Deleted!' % article.title, 'success')
    return redirect('/blog/')

@blogview.context_processor
def inject_navid():
    return dict(navid=moduleid)

navbar.add(moduleid, moduleid.title(), '/%s/' % moduleid)
