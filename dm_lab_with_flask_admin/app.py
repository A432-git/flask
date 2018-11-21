
from app import app, db
from app.model import User, Storage, Host, OperationSystem
import os

from werkzeug.security import generate_password_hash, check_password_hash
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

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

    # first_names = [
    #     'test', 'admin'
    # ]
    # last_names = [
    #     'test', 'admin'
    #
    # ]
    #
    # for i in range(len(first_names)):
    #     user = User()
    #     user.first_name = first_names[i]
    #     user.last_name = last_names[i]
    #     user.login = user.first_name.lower()
    #     user.email = user.login + "@example.com"
    #     user.password = generate_password_hash(''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10)))
    #     db.session.add(user)

    for temp in ['Unity','Rockies','VSA']:
        storage = Storage()
        storage.name = temp
        db.session.add(storage)

    for temp in ['Linux','Windows']:
        operation_system = OperationSystem()
        operation_system.name = temp
        db.session.add(operation_system)






    db.session.commit()
    return
# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    # app_dir = os.path.realpath(os.path.dirname(__file__))
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
