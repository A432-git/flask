#!flask/bin/python
from app import app
import os
app.config['SECRET_KEY'] = os.urandom(24) 
app.run(debug = True,host='0.0.0.0')