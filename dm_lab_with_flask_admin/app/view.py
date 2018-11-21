
from flask import  url_for, redirect, request
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from app import db,app
from .model import *
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
    column_editable_list = ['first_name', 'last_name','email']
    form_excluded_columns = ['password']
    can_delete = False
    column_searchable_list = ['login', 'email']


class MyObjectView(MyModelView):
    column_searchable_list = ['name']


# Customized Rig model admin
inline_form_options = {
    'form_label': "Properties",
    'form_columns': ['id', 'key', 'value'],
    'form_args': None,
    'form_extra_fields': None,
}


class RigView(MyObjectView):
    inline_models = [(RigInfo, inline_form_options), ]


class RigInfoVew(MyObjectView):
    column_searchable_list = ['rig_id']


init_login()

# Create admin
admin = admin.Admin(app, 'SPE-Data Mobility', index_view=MyAdminIndexView(), base_template='my_master.html')

# Add view
admin.add_view(MyUserView(User, db.session))

admin.add_view(MyObjectView(OperationSystem, db.session,category='Proto-Type'))
admin.add_view(MyObjectView(Storage, db.session,category='Proto-Type'))

admin.add_view(MyObjectView(Host, db.session,category='Lab'))
admin.add_view(RigView(Rig, db.session,category='Lab'))
admin.add_view(RigInfoVew(RigInfo, db.session,category='Lab'))
admin.add_view(MyModelView(IPAssignment, db.session,category='Lab'))
admin.add_view(MyObjectView(Virtualization, db.session,category='Lab'))
admin.add_view(MyObjectView(DataService, db.session,category='Lab'))

admin.add_view(MyObjectView(Testbed, db.session,category='Test'))
# admin.add_view(MyObjectView(Student, db.session,category='Test'))
# admin.add_view(MyObjectView(Course, db.session,category='Test'))


