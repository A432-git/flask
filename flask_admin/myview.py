# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午8:59
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : myview.py
# @Software: PyCharm
from flask_admin import BaseView, expose
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import FilterEqual


app = Flask(__name__)
db = SQLAlchemy(app)


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


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


# Customized User model admin
inline_form_options = {
    'form_label': "Info item",
    'form_columns': ['id', 'key', 'value'],
    'form_args': None,
    'form_extra_fields': None,
}


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='info')

    def __str__(self):
        return "{} - {}".format(self.key, self.value)


class UserAdmin(sqla.ModelView):
    action_disallowed_list = ['delete', ]
    column_display_pk = True
    column_list = [
        'id',
        'last_name',
        'first_name',
        'email',
        'pets',
    ]
    column_default_sort = [('last_name', False), ('first_name', False)]  # sort on multiple columns

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        FilterEqual(column=User.last_name, name='Last Name'),
    ]
    inline_models = [(UserInfo, inline_form_options), ]
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']
    column_searchable_list = [
        User.first_name,
        User.last_name,
        User.email,
    ]

    # setup create & edit forms so that only 'available' pets can be selected
    def create_form(self):
        return self._use_filtered_parent(
            super(UserAdmin, self).create_form()
        )

    def edit_form(self, obj):
        return self._use_filtered_parent(
            super(UserAdmin, self).edit_form(obj)
        )

    def _use_filtered_parent(self, form):
        form.pets.query_factory = self._get_parent_list
        return form

    def _get_parent_list(self):
        # only show available pets in the form
        return Pet.query.filter_by(available=True).all()

