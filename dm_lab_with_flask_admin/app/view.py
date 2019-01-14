from flask import url_for, redirect, request, jsonify
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
import json
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from .model import *
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class MyUserView(MyModelView):
    column_exclude_list = ['password', ]
    column_editable_list = ['first_name', 'last_name', 'email', 'phone']
    # hide the IP at phase I
    form_excluded_columns = ['password']
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['login', 'email', 'phone']


class MyObjectView(MyModelView):
    column_searchable_list = ['name']
    # pass


# Customized Rig model admin
inline_form_options = {
    'form_label': "Properties",
    'form_columns': ['id', 'key', 'value'],
    'form_args': None,
    'form_extra_fields': None,
}


class RigView(MyObjectView):
    inline_models = [(RigInfo, inline_form_options), ]
    column_exclude_list = ['io_interface', 'iscsi_interfaces', 'replication_async_interfaces',
                           'replication_sync_interfaces', 'state', 'status']
    column_editable_list = ['model', 'owner', 'device']
    inline_models = [(RigInfo, inline_form_options), ]
    column_extra_row_actions = [
        LinkRowAction('icon-eye-open', './{row_id}'),
        EndpointLinkRowAction('', 'rig.index_view')
    ]

    @expose('/<rig_id>')
    def show_chart(self, rig_id):
        rig = Rig.query.filter_by(id=rig_id).first()
        tbs = Testbed.query.all()
        rig_map_tb = []
        for item in tbs:
            print(f'tb_name :{item.name}')
            rigs = item.rigs
            for checked_rig in rigs:
                if rig.name == checked_rig.name:
                    rig_map_tb.append([rig.name, item.name, 'Used'])
        return self.render('rig.html', relation=rig_map_tb)


class RigInfoVew(MyObjectView):
    column_searchable_list = ['rig_id']


class TestBedView(MyObjectView):
    column_list = [
        'name',
        'owner',
        'rigs',
    ]
    form_excluded_columns = ['connect_chart', ]

    column_extra_row_actions = [
        LinkRowAction('icon-eye-open', './{row_id}'),
        EndpointLinkRowAction('', 'testbed.index_view')
    ]

    @expose('/<testbed_id>')
    def show_chart(self, testbed_id):
        tb = Testbed.query.filter_by(id=testbed_id).first()
        rigs = tb.rigs
        rig_names = [rig.name for rig in rigs]
        hosts = tb.hosts
        host_names = [host.name for host in hosts]
        rig_names.extend(host_names)
        if tb.connect_chart is None:
            relation_sample = []
        else:
            relation_sample = json.loads(tb.connect_chart)
        rig_connects = RigConnection.query.all()
        rig_connect_names = [rig_connect.name for rig_connect in rig_connects]
        host_usages = HostUsage.query.all()
        host_usage_names = [host_usage.name for host_usage in host_usages]
        rig_connect_names.extend(host_usage_names)
        return self.render('testbed2.html', rig_names=rig_names, tb_name=tb.name,
                           rig_connect_names=rig_connect_names,
                           relation=relation_sample)

    @expose('/save/<tb_name>', methods=['GET', 'POST'])
    def save(self, tb_name):
        print(tb_name)
        content = request.form.get('content')
        print(content)
        # print(Testbed.query.filter_by(name=tb_name).first())
        tb = Testbed.query.filter_by(name=tb_name).first()
        tb.connect_chart = content
        tb.save()
        return 'saved'

    #
    # def is_accessible(self):
    #     return login.current_user.is_authenticated

    # setup create & edit forms so that only 'available' pets can be selected
    # def create_form(self):
    #     return self._use_filtered_parent(
    #         super(TestBedView, self).create_form()
    #     )
    #
    # def edit_form(self, obj):
    #     return self._use_filtered_parent(
    #         super(TestBedView, self).edit_form(obj)
    #     )
    #
    # def _use_filtered_parent(self, form):
    #     form.rigs.query_factory = self._get_parent_list
    #     return form
    #
    # def _get_parent_list(self):
    #     # only show available pets in the form
    #     return Rig.query.filter_by(available=True).all()


class TestBedOrg(admin.BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    @expose('/')
    def index(self):
        tbs = Testbed.query.all()
        tbs_names = [tb.name for tb in tbs]
        rigs = Rig.query.all()
        rig_names = [rig.name for rig in rigs]
        # print(rigs)
        rig_connects = RigConnection.query.all()
        rig_connect_names = [rig_connect.name for rig_connect in rig_connects]

        return self.render('testbed.html', testbed_names=tbs_names, rig_names=rig_names,
                           rig_connect_names=rig_connect_names)

    @expose('/save/<tb_name>', methods=['GET', 'POST'])
    def save(self, tb_name):
        print(tb_name)
        content = request.form.get('content')
        print(content)
        # print(Testbed.query.filter_by(name=tb_name).first())
        tb = Testbed.query.filter_by(name=tb_name).first()
        tb.connect_chart = content
        tb.save()
        return 'saved'

    @expose('/get/<tb_name>')
    def get(self, tb_name):
        print(tb_name)
        tb = Testbed.query.filter_by(name=tb_name).first()
        rigs = tb.rigs
        rig_names = [rig.name for rig in rigs]
        if tb.connect_chart is None:
            relation_sample = []
        else:
            relation_sample = json.loads(tb.connect_chart)
        return jsonify(relation=relation_sample, rig_names=rig_names)


class testSetView(admin.BaseView):
    @expose('/')
    def index(self):
        return self.render('testset.html')


class testToolView(admin.BaseView):
    @expose('/')
    def index(self):
        return self.render('testtool.html')

init_login()

# Create admin
admin = admin.Admin(app, 'SPE-Data Mobility', index_view=MyAdminIndexView(),
                    base_template='my_master.html')

# Add view
admin.add_view(MyUserView(User, db.session))

admin.add_view(MyObjectView(OperationSystem, db.session, category='Proto-Type'))
admin.add_view(MyObjectView(Storage, db.session, category='Proto-Type'))
admin.add_view(MyObjectView(RigConnection, db.session, category='Proto-Type'))
admin.add_view(MyObjectView(HostUsage, db.session, category='Proto-Type'))

admin.add_view(MyObjectView(Host, db.session, category='Lab'))
admin.add_view(RigView(Rig, db.session, category='Lab'))
admin.add_view(RigInfoVew(RigInfo, db.session, category='Lab'))
# admin.add_view(MyModelView(IPAssignment, db.session,category='Lab'))
admin.add_view(MyObjectView(Virtualization, db.session, category='Lab'))
admin.add_view(MyObjectView(DataService, db.session, category='Lab'))

admin.add_view(TestBedView(Testbed, db.session, category='Test'))
admin.add_view(testSetView(name='Testset', category='Test'))
admin.add_view(testToolView(name='Testtool', category='Test'))
# admin.add_view(MyObjectView(Student, db.session,category='Test'))
# admin.add_view(MyObjectView(Course, db.session,category='Test'))

# admin.add_view(TestBedOrg(name='BedOrg', endpoint='bedorg',category='Test'))


