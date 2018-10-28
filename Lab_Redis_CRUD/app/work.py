
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import random
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///labmangement.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
lock = threading.RLock()


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ar_found = db.Column(db.Integer)
    ar_fix = db.Column(db.Integer)
    script = db.Column(db.Integer)
    cases = db.Column(db.Integer)
    version = db.Column(db.Integer)

    def __init__(self, _item):
        self.__dict__.update(_item)

    def __repr__(self):
        return f"Work {self.name} cases {self.cases} at {self.version}"

    def getVersion(self):
        lock.acquire()
        ver = self.version
        lock.release()
        return ver

    def save(self):
        message = f"Work {self.name}"
        lock.acquire()
        ownObj = Work.query.filter_by(name=self.name).first()
        if ownObj is None:
            self.__dict__.update({'version': 0})
            db.session.add(self)
            db.session.commit()
            message = f"{message} added successfully"
        else:
            message = f"{message} added by others already,please update!"
        lock.release()
        return message

    def delete(self):
        message = f"Work {self.name}"
        lock.acquire()
        ownObj = Work.query.filter_by(name=self.name).first()
        if not ownObj is None:
            db.session.delete(ownObj)
            db.session.commit()
            message = f"{message} deleted successfully"
        message = f"{message} deleted by others already,please update!"
        lock.release()
        return message

    def update(self, data, version):
        message = f"succeed to update {self.name} {data['cases']}"
        lock.acquire()
        tempWork = Work.query.filter_by(name=self.name).first()
        if version == tempWork.version:
            self.version += 1
            self.__dict__.update(data)
            try:
                db.session.merge(self)
                db.session.commit()
                lock.release()
            except:
                message = f"failed to update {self.name} "
            return f"{message} in thread {threading.currentThread().ident}"
        else:
            lock.release()
            return f"failed to update {self.name} in thread {threading.currentThread().ident} since others updated!"

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
            'ar_found': obj.ar_found,
            'ar_fix': obj.ar_fix,
            'name': obj.name,
            'script': obj.script,
            'cases': obj.cases,
            'version': obj.version
        }
    else:
        return obj


if __name__ == "__main__":
    # add new
    # nameList = ['reid_'+str(i) for i in range(10)]
    # nameList2 = ['alex_'+str(i) for i in range(10)]
    # nameList.extend(nameList2)
    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     futures = []
    #     for name in nameList:
    #         tempWork = Work({'name':name,'ar_found':random.randint(0,40),'ar_fix':random.randint(0,40),'script':random.randint(0,40),'cases':random.randint(0,40)})
    #         tempFutures = executor.submit(tempWork.save)
    #         futures.append(tempFutures)
    #     for future in as_completed(futures):
    #         print(future.result())
    # update
    # nameList = ['reid_'+str(i) for i in range(3)]

    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     temp = Work.query.filter_by(name='reid_0').first()
    #     version = temp.getVersion()
    #     temp1 = Work.query.filter_by(name='alex_0').first()
    #     version1 = temp1.getVersion()
    #     futures = [executor.submit(temp.update, {'cases':random.randint(0,100)},version) for i in range(10)]
    #     futures1 = [executor.submit(temp1.update, {'cases':random.randint(0,100)},version1) for i in range(10)]
    #     futures.extend(futures1)
    #     for future in as_completed(futures):
    #         print(future.result())

    # delete in mul-threading
    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     temp = Work.query.filter_by(name='reid_0').first()
    #     version = temp.getVersion()
    #     temp1 = Work.query.filter_by(name='alex_0').first()
    #     version1 = temp1.getVersion()
    #     futures = [executor.submit(temp.delete) for i in range(10)]
    #     futures1 = [executor.submit(temp1.delete) for i in range(10)]
    #     futures.extend(futures1)
    #     for future in as_completed(futures):
    #         print(future.result())
    # temp = Work.query.filter_by(name='reid_0').first()
    # dict_json = temp.getJson()
    # print(dict_json)
    # temp.update({'cases':110})
    # print(work.version)
    # print(work.getJson())
    # print(work.version)
    # tempWork.update({'cases':120})
    # {'ar_found': 32, 'ar_fix': 16, 'name': 'reid_8', 'script': 39,
    #  # 'cases': 19, 'version': 0}
    temp = Work.query.filter_by(name='reid_8', ar_fix=16).first()
    print(temp)
    # works = Work.query.all()
    # for work in works:
    #         print(work.getJson())
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
    # works = Work.query.all()
    # for work in works:
    # print(work.getJson())
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