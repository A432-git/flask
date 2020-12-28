# -*- coding: utf-8 -*-
# @Time    : 18-11-17 下午3:29
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : views.py
# @Software: PyCharm
from .model import Case
from app import db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose,AdminIndexView


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class CaseAdmin(sqla.ModelView):
    action_disallowed_list = ['delete', ]
    column_display_pk = True
    column_list = [
        'project',
        'plan',
        'tc_id',
        'result',
        'bug',
        'executor',
        'execute_date'
    ]
    column_default_sort = [('execute_date', False), ]  # sort on multiple columns

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        FilterEqual(column=Case.tc_id, name='TC_ID'),
    ]
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']
    column_searchable_list = [
        Case.tc_id,
        Case.plan,
        Case.project,
        Case.result
    ]
    column_editable_list = ['bug', 'result']
    create_modal = True
    edit_modal = True
    can_view_details = True
    # setup create & edit forms so that only 'available' pets can be selected
    # def create_form(self):
    #     return self._use_filtered_parent(
    #         super(CaseAdmin, self).create_form()
    #     )

    # def edit_form(self, obj):
    #     return self._use_filtered_parent(
    #         super(CaseAdmin, self).edit_form(obj)
    #     )


# admin = Admin(app, name='SPE DJY', template_mode='bootstrap3')
admin = Admin(
    app,
    name='CMII-研一测试',
    index_view=AdminIndexView(
        name='主页',
        template='index.html',
        url='/admin'
    )
)
# admin.add_view(MyView(name='Hello'))
# seems py3.7 not support FileAdmin
# path = op.join(op.dirname(__file__), 'static')
# admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
# admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
# admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(CaseAdmin(Case, db.session, category="Lab"))
