# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午8:49
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : myapp.py
# @Software: PyCharm
from flask import Flask
from flask_admin import Admin
from myview import MyView,UserAdmin,User,Pet
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os.path as op


app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
admin = Admin(app, name='SPE DJY', template_mode='bootstrap3')
admin.add_view(MyView(name='Hello'))
# Add administrative views here
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


admin.add_view(UserAdmin(User, db.session,category="Lab"))
admin.add_view(ModelView(Pet, db.session,category="Lab"))
app.run(debug = True,host='0.0.0.0')