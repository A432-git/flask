from app import db
class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.name


class OperationSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.name

# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    def __str__(self):
        return self.login
    # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    operation_system_id = db.Column(db.Integer(), db.ForeignKey(OperationSystem.id))
    operation_system = db.relationship(OperationSystem, backref='hosts')
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Owner = db.relationship(User, backref='hosts')

    def __str__(self):
        return self.name


# Create rig model
class Rig (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    device_id = db.Column(db.Integer(), db.ForeignKey(Storage.id))
    device = db.relationship(Storage, backref='rigs')
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Owner = db.relationship(User, backref='rigs')

    def __str__(self):
        return self.name


class TestBed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Owner = db.relationship(User, backref='testbeds')
    rig_id = db.Column(db.Integer(), db.ForeignKey(Rig.id))
    rigs = db.relationship(Rig, backref='testbeds')

