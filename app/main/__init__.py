#!usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'woodenrobot'


from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors