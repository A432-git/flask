# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:11
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : model.py
# @Software: PyCharm
from app import db


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100))
    plan = db.Column(db.String(100))
    tc_id = db.Column(db.String(100))
    result = db.Column(db.Enum(
        'No Run', 'Passed', 'Failed', 'Blocked'), server_default='No Run', nullable=False)
    bug = db.Column(db.String(100))
    detail = db.Column(db.String(200))
    execute_date = db.Column(db.DateTime())
    logs = db.Column(db.String(100))
    executor = db.Column(db.String(10))
    def __str__(self):
        return "{}".format(self.tc_id)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())



