#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'


from . import db, login_manager
from datetime import datetime
from markdown import markdown
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User> %r' % User.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    title = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        if self.category is None:
            self.category = Category.query.filter_by(name='无').first()

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2' ,'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_change_body)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    @staticmethod
    def insert_categories():
        categories = ['杂谈', '技术', '爱好']

        for v in categories:
            category = Category.query.filter_by(name=v).first()
            if category is None:
                category = Category(name=v)
            db.session.add(category)
        db.session.commit()

    def __repr__(self):
        return '<Category> %r' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
