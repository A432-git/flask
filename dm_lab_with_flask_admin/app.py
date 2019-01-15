
from app import app, db
from app.model import User, Storage, Host, OperationSystem, RigConnection, Rig
import os

from werkzeug.security import generate_password_hash, check_password_hash



# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to SPE Data Mobility Admin!</a>'


@app.route('/rest_for_jia/<obj_name>/<name>/<obj_property>/<obj_value>', methods=['get', 'post'])
def rest_for_jia(obj_name, name, obj_property, obj_value):
    try:
        module = __import__(f'app.model')
        obj_name = obj_name[0].upper() + obj_name[1:]
        reflected_class = getattr(module, obj_name)()
        obj = reflected_class.query.filter_by(name=name).first()
        if obj:
            if hasattr(obj, obj_property):
                setattr(obj, obj_property, obj_value)
            else:
                raise AttributeError('property not exist')
        else:
            raise AttributeError('record not exist')
        db.session.commit()
        return "succeed"
    except AttributeError:
        return 'Fail'









if __name__ == '__main__':
    # Start app
    app.run(debug=False, host='0.0.0.0')
