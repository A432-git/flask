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


class RigConnection(db.Model):
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
    model = db.Column(db.String(100))

    def __str__(self):
        return self.name


tags = db.Table('tags',
                           db.Column('testbed_id', db.Integer, db.ForeignKey('testbed.id')),
                           db.Column('rig_id', db.Integer, db.ForeignKey('rig.id'))
                           )

# tags=db.Table('tags',db.Column('testbed_id',db.Integer,db.ForeignKey('testbed.id')),db.Column('rig_id',db.Integer,db.ForeignKey('rig.id')))


class Testbed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship(User, backref='testbeds')
    rig_id = db.Column(db.Integer, db.ForeignKey('rig.id'))
    rigs = db.relationship('Rig', secondary=tags)
    # tags = db.relationship('Tag', secondary=post_tags_table)
    connect_chart = db.Column(db.String(100))

    def __str__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

# Create rig model
class Rig (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    device_id = db.Column(db.Integer(), db.ForeignKey(Storage.id))
    device = db.relationship(Storage, backref='rigs')
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship(User, backref='rigs')
    model = db.Column(db.String(100),default='Unity 550F')
    available = db.Column(db.Boolean)

    def __str__(self):
        return self.name


class RigInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    rig_id = db.Column(db.Integer(), db.ForeignKey(Rig.id))
    rig = db.relationship(Rig, backref='info')


class IPAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipv4 = db.Column(db.String(100), unique=True)
    ipv4_mask = db.Column(db.String(100), default='255.255.255.0')
    ipv4_gateway = db.Column(db.String(100), default='10.109.104.1')
    ipv6 = db.Column(db.String(100), unique=True)
    ipv6_mask = db.Column(db.String(100))
    ipv6_gateway = db.Column(db.String(100))
    vlan = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref='ips')

    def __str__(self):
        return f'{self.ipv4}-{self.ipv6}'


class DataService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    server_ip = db.Column(db.String(100))
    credential = db.Column(db.String(300))


class Virtualization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    ip = db.Column(db.String(100))
    credential = db.Column(db.String(300))
    vcenter = db.Column(db.String(100), default='10.109.118.23')






