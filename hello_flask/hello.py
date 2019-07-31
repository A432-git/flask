#!/usr/bin/python
# encoding: utf-8
"""
@author: yangr5 
@contact: yangtao584@126.com
@version: 1.0
@license: Apache Licence
@file: hello.py
@time: 2019-07-16 22:04

这一行开始写关于本文件的说明与解释
"""
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello flask'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

