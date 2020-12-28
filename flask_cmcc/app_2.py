# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:18
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : app_2.py
# @Software: PyCharm
from app import app,db
from app.model import Case
import os,json,datetime
import os.path as op
from flask import request,jsonify


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'cmii_research_1_test.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

@app.route('/test', methods=['POST'])
def post_Data():
    # print('hh')
    data = request.get_data()

    data = json.loads(data)
    print(type(data.get('execute_date')))
    c = Case()
    c.tc_id = data.get('tc_id')
    c.project = data.get('project')
    c.plan = data.get('plan')
    c.detail = data.get('detail')
    c.result = data.get('result')
    c.executor = data.get('executor')
    c.execute_date = datetime.datetime.strptime(data.get('execute_date'), '%Y-%m-%d %H:%M:%S')
    db.session.add(c)
    db.session.commit()

    # numb = int(data.get('numb'))
    #
    # numb += 1
    # return str(numb)
    #
    # recognize_info = {'id': postdata}
    return {'code':200,'id': data}


if __name__ == '__main__':

    app_dir = op.realpath(os.path.dirname(__file__))
    print(app_dir)
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    print(database_path)
    # if not os.path.exists(database_path):
    #     build_db()
    # app.run(debug = True,host='0.0.0.0')
    # print(Case.query.all())
    # c = Case()
    # c.tc_id = 'test_1002'
    # c.plan =''
    # db.session.add(c)
    # db.session.commit()
    # print(Case.query.all())
    app.run(debug=False, host='0.0.0.0', port=5001)