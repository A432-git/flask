# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:26
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
# set optional bootswatch theme

from .model import *
from .views import *
