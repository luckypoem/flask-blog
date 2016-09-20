#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'


from app import db
from . import main
from flask import url_for, render_template, request, flash, redirect
from flask_login import login_required
from ..models import Post, Category
from .forms import PostForm


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@main.route('/nothing')
def nothing():
    category = Category.query.filter_by(name='杂谈').first()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category=category).order_by(
        Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/technology')
def technology():
    category = Category.query.filter_by(name='技术').first()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category=category).order_by(
        Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/favorite')
def favorite():
    category = Category.query.filter_by(name='爱好').first()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category=category).order_by(
        Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = Category.query.filter_by(id=form.category.data)\
            .first()
        post.body = form.body.data
        db.session.add(post)
        flash('文章修改成功')
        return redirect(url_for('main.post', id=post.id))
    form.title.data = post.title
    if post.category:
        form.category.data = post.category.id
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    category=Category.query.filter_by(id=form.category.data)\
                    .first(),
                    body=form.body.data)
        db.session.add(post)
        flash('文章创建成功')
        return redirect(url_for('.index'))
    return render_template('new_post.html', form=form)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    return redirect(url_for('main.index'))
