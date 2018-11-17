# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午8:59
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : myview.py
# @Software: PyCharm
from flask_admin import BaseView, expose


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')



