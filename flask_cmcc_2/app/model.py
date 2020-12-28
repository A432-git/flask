# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:11
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : model.py
# @Software: PyCharm
from app import db


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    projects = db.relationship('Project', backref='belongs')

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    available = db.Column(db.Boolean)

    def __str__(self):
        return self.name

# Customized User model admin
inline_form_options = {
    'form_label': "Info item",
    'form_columns': ['id', 'key', 'value'],
    'form_args': None,
    'form_extra_fields': None,
}


class CaseInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    case_id = db.Column(db.Integer(), db.ForeignKey(Case.id))
    case = db.relationship(Case, backref='info')

    def __str__(self):
        return "{} - {}".format(self.key, self.value)