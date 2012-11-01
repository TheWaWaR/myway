#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, redirect, url_for, flash, request
from myway.utils import db, navbar
from myway.common.login import current_user

from .models import Article
from .forms import ArticleForm

moduleid = 'blog'
blogview = Blueprint(moduleid, __name__, url_prefix='/' + moduleid)

@blogview.route('/')
def index():
    LIMIT = 8
    key = request.args.get('key', '')
    
    query = Article.query
    if current_user.is_anonymous():
        query = query.filter(db.and_(Article.status==3,
                                     Article.visibility < 3))
    if key:
        ikey = '%' + key + '%'
        query = query.filter(db.or_(Article.title.ilike(ikey),
                                    Article.md_content.ilike(ikey)))
    articles = query.order_by(Article.created_at.desc())\
                            .offset(0).limit(LIMIT).all()
    return render_template('blog/index.html', articles=articles, key=key)


@blogview.route('/<int:id>')
def single(id):
    article = Article.query.get_or_404(id)
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
    return render_template('blog/new-edit.html', form=form,
                           action=url_for('blog.new'), title=u'New Article')


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
    return render_template('blog/new-edit.html', form=form,
                           action=url_for('blog.edit', id=id),
                           view_link=url_for('blog.single', id=id),
                           title=u'Edit: %s' % article.title)


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
