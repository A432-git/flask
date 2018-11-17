# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:11
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : model.py
# @Software: PyCharm
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pets = db.relationship('Pet', backref='owner')

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    available = db.Column(db.Boolean)

    def __str__(self):
        return self.name

