from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///labmangement.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ar_found = db.Column(db.Integer)
    ar_fix = db.Column(db.Integer)
    script = db.Column(db.Integer)
    cases = db.Column(db.Integer)

    def __init__(self, _item):
        # self.id=_item['id']
        # self.name=_item['name']
        # self.price=_item['price']
        self.__dict__.update(_item)  

    def __repr__(self):
        return '<Work %r>' % self.name
    
        
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
    def getWork(json_str):
        return json.loads(json_str, cls=userDecode)


class userDecode(json.JSONDecoder):
    def decode(self, s):
        dic = super().decode(s)
        return Work(dic)
        
def obj2dict(obj):

    if (isinstance(obj, Work)):
        return {
            'ar_found':obj.ar_found,
            'ar_fix':obj.ar_fix,
            'name': obj.name,
            'script':obj.script,
            'cases':obj.cases
        }
    else:
        return obj  

#
# work = {'name':'cherry','ar_found':88,'ar_fix':40,'script':50,'cases':80}
# admin=Work(work)
# print(admin.name)
# admin.save()
if __name__ == "__main__":
    # nameList = ['alex_'+str(i) for i in range(100)]
    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     futures = []
    #     for name in nameList:
    #         tempWork = Work({'name':name,'ar_found':random.randint(0,40),'ar_fix':random.randint(0,40),'script':random.randint(0,40),'cases':random.randint(0,40)})
    #         tempFutures = executor.submit(tempWork.save())
    #         futures.append(tempFutures)
    #     for future in as_completed(futures):
    #         pass
    #
    # work = Work.query.filter_by(name='cherry').first()
    # if( not work is None):
    #     print(work.name)
    #     work.name = 'reid'
    #     work.update()
    #     print(work.name)
    # else:
    #     print('not found')

    # uobj= admin.getJson()
    # lists = list(uobj.keys())
    # print( lists)
    # lists.remove('name')
    # print(lists)
    # print(json.dumps(uobj))
    # u2 = json.loads(json.dumps(uobj), cls=userDecode)
    # print('Work: ', u2)
    # admin.save()

    # db.create_all() # In case user table doesn't exists already. Else remove it.

    # db.session.save(admin)

    # db.session.commit() # This is needed to write the changes to database
    # data=[]
    works = Work.query.all()
    for work in works:
            print(work.getJson())
    #         # post = dict(zip(['id','name','price'],[ item.id,str(item.name, encoding = "utf-8")  ,str(item.price, encoding = "utf-8") ]))
    #         # data.append(post)
    #         print(work.getJson().keys())
    #         data.append(work.getJson())
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