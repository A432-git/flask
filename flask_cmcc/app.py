# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:18
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : app.py
# @Software: PyCharm
from app import app,db
from app.model import Case
import os
import os.path as op


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'cmii_research_1_test.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


def build_db():
    db.drop_all()
    db.create_all()
    case_list = []
    for i in range(10):
        case = Case()
        case.tc_id = 'test_'+str(i+1)

        # case_list.append(case)
        db.session.add(case)

    db.session.commit()
    return


if __name__ == '__main__':

    app_dir = op.realpath(os.path.dirname(__file__))
    print(app_dir)
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_db()
    app.run(debug = True,host='0.0.0.0')