# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:29
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : views.py
# @Software: PyCharm
from .model import Case,Project,inline_form_options, CaseInfo
from app import db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class CaseAdmin(sqla.ModelView):
    action_disallowed_list = ['delete', ]
    column_display_pk = True
    column_list = [
        'id',
        'name',
        'projects',
    ]
    column_default_sort = [('name', False), ]  # sort on multiple columns

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        FilterEqual(column=Case.name, name='Name'),
    ]
    inline_models = [(CaseInfo, inline_form_options), ]
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']
    column_searchable_list = [
        Case.name,

    ]

    # setup create & edit forms so that only 'available' pets can be selected
    def create_form(self):
        return self._use_filtered_parent(
            super(CaseAdmin, self).create_form()
        )

    def edit_form(self, obj):
        return self._use_filtered_parent(
            super(CaseAdmin, self).edit_form(obj)
        )

    def _use_filtered_parent(self, form):
        form.projects.query_factory = self._get_parent_list
        return form

    def _get_parent_list(self):
        # only show available pets in the form
        return Project.query.filter_by(available=True).all()


admin = Admin(app, name='SPE DJY', template_mode='bootstrap3')
admin.add_view(MyView(name='Hello'))
# seems py3.7 not support FileAdmin
# path = op.join(op.dirname(__file__), 'static')
# admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(CaseAdmin(Case, db.session, category="Lab"))
admin.add_view(ModelView(Project, db.session, category="Lab"))
