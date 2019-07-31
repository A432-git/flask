#!/usr/bin/env python
# encoding: utf-8


"""
@version: 0.1
@author: Yang Reid
@license: Apache Licence 
@contact: yangtao584@126.com
@site: https://github.com/yangr5/python
@software: PyCharm
@file: app.py
@time: 2019/7/11 10:42
"""
from flask import Flask,render_template,jsonify,json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dom')
def index_dom():
    return render_template('index_dom.html')

@app.route('/dom2')
def index_search():
    return render_template('index_dom_2.html')

@app.route('/button')
def index_button():
    return render_template('button.html')

@app.route('/ydacf')
def ydacf():
    return  render_template('ydacf.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')