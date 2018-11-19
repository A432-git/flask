from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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


tags = db.Table('tags',db.Model.metadata,
                           db.Column('testbed_id', db.Integer, db.ForeignKey('testbed.id')),
                           db.Column('rig_id', db.Integer, db.ForeignKey('rig.id'))
                           )

# tags=db.Table('tags',db.Column('testbed_id',db.Integer,db.ForeignKey('testbed.id')),db.Column('rig_id',db.Integer,db.ForeignKey('rig.id')))


class Testbed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Owner = db.relationship(User, backref='testbeds')
    rigs = db.relationship('Rig', secondary=tags)
    # tags = db.relationship('Tag', secondary=post_tags_table)


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


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")
    test_user = User(login="test", password=generate_password_hash("test"))
    db.session.add(test_user)

    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]

    for i in range(len(first_names)):
        user = User()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.login = user.first_name.lower()
        user.email = user.login + "@example.com"
        user.password = generate_password_hash(''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10)))
        db.session.add(user)

    db.session.commit()
    return


build_sample_db()
