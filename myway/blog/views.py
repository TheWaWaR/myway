#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint, render_template, request, redirect, url_for, flash
from myway.utils import db

from .models import Article, Category
from .forms import ArticleForm

blogview = Blueprint('blog', __name__, url_prefix='/blog')

@blogview.route('/')
def index():
    LIMIT = 5
    articles = Article.query.order_by(Article.created_at.desc())\
                            .offset(0).limit(LIMIT).all()
    return render_template('blog/index.html', articles=articles)


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
        return redirect(url_for('blog.edit', id=article.id))
    form.process(obj=article)
    return render_template('blog/new-edit.html', form=form,
                           action=url_for('blog.edit', id=id), title=u'Edit Article')
