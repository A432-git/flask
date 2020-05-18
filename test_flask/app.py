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
from flask import Flask,render_template,jsonify,request
from redisworks import Root

root = Root(host='18.221.249.189')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ajax/get_dm_array')
def ajax_rigs():
    return jsonify(data=list(root.dm.array))

@app.route('/rigs')
def rigs():
    return render_template('rig.html')
    # return render_template('test_case_responsive.html')


@app.route('/ajax/get_tc_status')
def ajax_tc_status():
    data = list(root.Goshawk_overall_status)
    return jsonify(data=data)


@app.route('/ajax/get_tc_note/<configuration_name>')
def ajax_tc_note(configuration_name):
    if root[configuration_name]:
        return jsonify(str(root[configuration_name]))
    else:
        return jsonify('')

@app.route('/ajax/set_tc_note/<configuration_name>',methods = ['POST'])
def ajax_set_tc_note(configuration_name):
    note = request.form.get('note')
    root[configuration_name] = note
    return jsonify(configuration_name)

@app.route('/test_case')
def test_case_status():
    return render_template('test_case.html')

@app.route('/reid_test')
def test_reid():
    return render_template('popup_info.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')