
from app import app, db
from app.model import User, Storage, Host, OperationSystem, RigConnection, Rig
import os

from werkzeug.security import generate_password_hash, check_password_hash
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = '../data/spe_djy_lab.sqlite'
# this is for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
# this is for mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@Baidu123@localhost:3306/test'
app.config['SQLALCHEMY_ECHO'] = True


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to SPE Data Mobility Admin!</a>'


if __name__ == '__main__':
    # Start app
    app.run(debug=True)
