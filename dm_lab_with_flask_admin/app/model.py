from app import db
import json


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    # sub_model = db.Column(db.String(100))

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return json.dumps({'name': self.name})


class OperationSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps({'name': self.name})


class RigConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps({'name': self.name})


class HostUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps({'name': self.name})


# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    def __str__(self):
        return self.login

    def __repr__(self):
        return json.dumps({'name': self.login})

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
    name = db.Column(db.String(100))
    operation_system_id = db.Column(db.Integer(), db.ForeignKey(OperationSystem.id))
    operation_system = db.relationship(OperationSystem, backref='hosts')
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Owner = db.relationship(User, backref='hosts')
    usage_id = db.Column(db.Integer(), db.ForeignKey(HostUsage.id))
    usage = db.relationship(HostUsage,backref='hosts')
    ip = db.Column(db.String(20), unique=True)
    available = db.Column(db.Boolean(),default=True)
    # tag = db.Column(db.String(20))

    def __str__(self):
        return self.ip

    def __repr__(self):
        return json.dumps({
            'name': repr(self.name),
            'usage': repr(self.usage),
            'ip': repr(self.ip),
            'available': repr(self.available),
            'operation_system': repr(self.operation_system),
        })


rig_tags = db.Table('rig_tags',
                           db.Column('testbed_id', db.Integer, db.ForeignKey('testbed.id')),
                           db.Column('rig_id', db.Integer, db.ForeignKey('rig.id'))
       )

host_tags = db.Table('host_tags',
                           db.Column('testbed_id', db.Integer, db.ForeignKey('testbed.id')),
                           db.Column('host_id', db.Integer, db.ForeignKey('host.id'))
       )


class Testbed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship(User, backref='testbeds')
    rig_id = db.Column(db.Integer, db.ForeignKey('rig.id'))
    rigs = db.relationship('Rig', secondary=rig_tags)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    hosts = db.relationship('Host', secondary=host_tags)
    connect_chart = db.Column(db.String(300))
    tags = db.Column(db.String(20))

    def __str__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):

        return json.dumps({
            'name': self.name,
            'tags': self.tags,
            'rigs': repr(self.rigs),
            'hosts': repr(self.hosts),
            'connect_chart': repr(self.connect_chart),
        })


# Create rig model
class Rig (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    device_id = db.Column(db.Integer(), db.ForeignKey(Storage.id))
    device = db.relationship(Storage, backref='rigs')
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship(User, backref='rigs')
    model = db.Column(db.String(100),default='Unity 550F')
    available = db.Column(db.Boolean,default=True)
    state = db.Column(db.String(30))
    status = db.Column(db.String(30))
    io_interfaces = db.Column(db.Text)
    iscsi_interfaces = db.Column(db.Text)
    replication_async_interfaces = db.Column(db.Text)
    replication_sync_interfaces = db.Column(db.Text)

    def __str__(self):
        return self.name

    def __repr__(self):

        return json.dumps({
            'name': repr(self.name),
            'state': repr(self.state),
            'status': repr(self.status),
            'available': repr(self.available),
            'io_interfaces': repr(self.io_interfaces),
            'iscsi_interfaces': repr(self.iscsi_interfaces),
            'replication_async_interfaces': repr(self.replication_async_interfaces),
            'replication_sync_interfaces': repr(self.replication_sync_interfaces)
        })


class RigInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    rig_id = db.Column(db.Integer(), db.ForeignKey(Rig.id))
    rig = db.relationship(Rig, backref='info')

    def __repr__(self):
        return json.dumps({
            self.key: self.value

        })


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

