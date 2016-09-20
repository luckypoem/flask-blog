#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'


from flask_wtf import Form
from wtforms import SubmitField, StringField, SelectField
from flask_pagedown.fields import PageDownField
from ..models import Category


class PostForm(Form):
    title = StringField('标题')
    category = SelectField('分类', coerce=int)
    body = PageDownField('内容')
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(
                Category.name).all()]
