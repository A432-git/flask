from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@Baidu123@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.String(50), unique=True)

    def __init__(self, _item):
        # self.id=_item['id']
        # self.name=_item['name']
        # self.price=_item['price']
        self.__dict__.update(_item)  

    def __repr__(self):
        return '<Item %r>' % self.name
    
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        message = "succeed to update "+self.name
        try:
            db.session.merge(self)
            db.session.commit()
        except:
            message = "failed to update "+self.name
        return message
            
    def getJson(self):
        return json.loads(json.dumps(obj2dict(self)))
    
    @staticmethod
    def getItem(json_str):
        return json.loads(json_str, cls=userDecode)

class userDecode(json.JSONDecoder):
    def decode(self, s):
        dic = super().decode(s)
        return Item(dic['id'], dic['name'],dic['price'])
        
def obj2dict(obj):

    if (isinstance(obj, Item)):
        return {
            'id':obj.id,
            'name': obj.name,
            'price': obj.price
        }
    else:
        return obj  

    
# item = {'name':'test101','price':'$101'}
# print(item['id'])
# admin=Item(item)
# print(admin.name)
# admin.save()
# for i in range(7,100):
    # name = 'test'+ str(i)
    # price = '$' +str(i)
    # print('name' + name)
    # admin = Item(i, name, price)
    # admin.save()
# init fun1
# item={'id':7,'name':'test7','price':'$7'}
# u = Item(item)
# print(u)
# uobj = json.dumps(obj2dict(u))
# uobj= u.getJson()
# print( uobj['id'])
# uobj=json.loads(uobj)
# print(uobj['id'])
# u2=Item(uobj)
# print(u2)
# u2 = Item.getItem(uobj)
# print(u2)
# u2 = json.loads(uobj, cls=userDecode)
# print('Item: ', u2)
# admin.save()

# db.create_all() # In case user table doesn't exists already. Else remove it.    

# db.session.save(admin)

# db.session.commit() # This is needed to write the changes to database
# data=[]
# items = Item.query.all()
# for item in items:
        # print(item)
        # post = dict(zip(['id','name','price'],[ item.id,str(item.name, encoding = "utf-8")  ,str(item.price, encoding = "utf-8") ]))
        # data.append(post)
        # print(item.getJson())
        # data.append(item.getJson())
# print(data)
# item = Item.query.filter_by(name='test4').first()
# if( not item is None):
    # print(item.name)
    # item.name = 'reid'
    # item.update()
    # print(item.name)
# else:
    # print('not found')
# db.session.merge(item)
# db.session.commit()
# print(item.name)