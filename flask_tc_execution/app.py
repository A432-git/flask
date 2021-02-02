import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

from wtforms import validators

import flask_admin as admin
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.contrib.sqla.fields import InlineModelFormList
from flask_admin import BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual


# Create application
app = Flask(__name__)

# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'case_execution.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100))
    plan = db.Column(db.String(100))
    tc_id = db.Column(db.String(100))
    result = db.Column(db.Enum(
        'No Run', 'Passed', 'Failed', 'Blocked'), server_default='No Run', nullable=False)
    version = db.Column(db.String(100))
    bug = db.Column(db.String(100))
    detail = db.Column(db.String(200))
    execute_date = db.Column(db.DateTime())
    logs = db.Column(db.String(100))
    executor = db.Column(db.String(10))

    def __str__(self):
        return "{}".format(self.tc_id)

    def __repr__(self):
        return "{}: {}".format(self.id, self.__str__())


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
        'version',
        'bug',
        'executor',
        'execute_date'
    ]
    column_default_sort = [('execute_date', False), ]  # sort on multiple columns

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        FilterEqual(column=Case.tc_id, name='TC_ID'),
        FilterEqual(column=Case.project, name='Project'),
        FilterEqual(column=Case.plan, name='Plan'),
        FilterEqual(column=Case.version, name='Version'),
        FilterEqual(column=Case.executor, name='Executor'),
    ]
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']
    column_searchable_list = [
        Case.tc_id,
        Case.plan,
        Case.project,
        Case.result,
        Case.version
    ]
    column_editable_list = ['bug', 'result']
    create_modal = True
    edit_modal = True
    can_view_details = True

# Create admin
admin = admin.Admin(app, name='CMII--研发一部', template_mode='bootstrap3')
admin.add_view(CaseAdmin(Case, db.session, category="Lab"))

# Add views

def build_sample_db():
    db.drop_all()
    db.create_all()
    case_list = []
    for i in range(10):
        case = Case()
        case.tc_id = 'test_' + str(i + 1)

        # case_list.append(case)
        db.session.add(case)

    db.session.commit()
    return


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    # app_dir = op.realpath(os.path.dirname(__file__))
    # database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    #     build_sample_db()

    # Start app
    app.run(debug=True)
