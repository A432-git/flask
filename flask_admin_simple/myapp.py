# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午8:49
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : myapp.py
# @Software: PyCharm
from flask import Flask
from flask_admin import Admin
from myview import MyView
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import FilterEqual

app = Flask(__name__)
db = SQLAlchemy(app)
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

admin = Admin(app, name='SPE DJY', template_mode='bootstrap3')
admin.add_view(MyView(name='Hello'))
# Add administrative views here
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


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


admin.add_view(UserAdmin(User, db.session,category="Lab"))
admin.add_view(ModelView(Pet, db.session,category="Lab"))
app.run(debug = True,host='0.0.0.0')