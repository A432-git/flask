from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = '../data/spe_djy_lab.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this is for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
# this is for mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@Baidu123@localhost:3306/test'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# set optional bootswatch theme

from .model import *
from .view import *

