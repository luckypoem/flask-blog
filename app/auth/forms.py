#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'


from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import data_required, Length


class LoginForm(Form):
    username = StringField('username', validators=[data_required(),
                                                   Length(1, 64)])
    password = PasswordField('password', validators=[data_required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')