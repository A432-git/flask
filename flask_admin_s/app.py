# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:18
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : app.py
# @Software: PyCharm
from app import app
from flask import Flask


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0')