# -*- coding: utf-8 -*-
# @Time    : 18-11-16 下午11:51
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : app.py
# @Software: PyCharm
import os
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

# init Flask
app = Flask(__name__)

# Basic config with security for forms and session cookie
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'thisismyscretkey'

# Init SQLAlchemy
db = SQLA(app)
# Init F.A.B.
appbuilder = AppBuilder(app, db.session)

# Run the development server
app.run(host='0.0.0.0', port=5000, debug=True)