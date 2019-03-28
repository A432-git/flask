
from app import *
from flask import jsonify


def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('_') and not callable(value) \
                and not name.startswith('meta') and not name.startswith('query'):
            # print(f"name:{name}")
            pr[name] = repr(value)
    return pr


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to SPE Data Mobility Admin!</a>'

@app.route('/api/get/<obj_name>')
def rest_getlist(obj_name):
    module = __import__(f'app.model')
    obj_name = obj_name[0].upper() + obj_name[1:]
    reflected_class = getattr(module, obj_name)()
    objs = reflected_class.query.all()
    obj_names = [obj.name for obj in objs]
    return jsonify(obj_names)
    
    
@app.route('/api/get/<obj_name>/<name>')
def rest_get(obj_name, name):
    module = __import__(f'app.model')
    obj_name = obj_name[0].upper() + obj_name[1:]
    reflected_class = getattr(module, obj_name)()
    obj = reflected_class.query.filter_by(name=name).first()
    print(props(obj))
    return jsonify(props(obj))
    # return repr(obj)

@app.route('/api/get/<obj_name>/<name>/<obj_property>')
def rest_getone(obj_name, name, obj_property):
    module = __import__(f'app.model')
    obj_name = obj_name[0].upper() + obj_name[1:]
    reflected_class = getattr(module, obj_name)()
    obj = reflected_class.query.filter_by(name=name).first()
    property_value = getattr(obj, obj_property)
    return jsonify({obj_property: property_value})


@app.route('/api/set/<obj_name>/<name>/<obj_property>/<obj_value>', methods=['get', 'post'])
def rest_set(obj_name, name, obj_property, obj_value):
    try:
        module = __import__(f'app.model')
        obj_name = obj_name[0].upper() + obj_name[1:]
        reflected_class = getattr(module, obj_name)()
        obj = reflected_class.query.filter_by(name=name).first()
        if obj:
            if hasattr(obj, obj_property):
                if obj_property == 'available':
                    if obj_value == 'true' or obj_value == 'True':
                        setattr(obj, obj_property, True)
                    else:
                        setattr(obj, obj_property, False)
                else:
                    setattr(obj, obj_property, obj_value)
            else:
                raise AttributeError('property not exist')
        else:
            raise AttributeError('record not exist')
        db.session.commit()
        return jsonify(result="succeed")
    except AttributeError:
        return jsonify(result="fail")


if __name__ == '__main__':
    # Start app
    app.run(debug=False, host='0.0.0.0')
