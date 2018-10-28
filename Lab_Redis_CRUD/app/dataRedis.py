import redis   
import json
class DataRedis():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    root = redis.Redis(connection_pool=pool)
    def __init__(self,dataName,_item):
        
        self.dataName = dataName
        self.redisFormat = "root.{}.{}".format(dataName,_item[0])
        self.content = json.dumps(_item)
        # self.__dict__.update(_item)
    
    def save(self):
        DataRedis.root.set(self.redisFormat,self.content)
        
    def delete(self):
        DataRedis.root.delete(self.redisFormat)
    
    @staticmethod        
    def queryAll(dataName):
        all = []
        for key in DataRedis._getAllKey(dataName):
            data_json_str = DataRedis.root.get(key)
            # print(data_json_str) 
            # print(type(data_json_str))
            # print(data_json_str[0])
            dataItem = json.loads(data_json_str)
            print(type(dataItem))
            all.append(dataItem)
        return all
            # print(type(json.loads(data_json_str)))
    
    @staticmethod
    def _getAllKey(dataName):
        dataName = "*{}*".format(dataName)
        return DataRedis.root.keys(dataName)

d = DataRedis('rig',['OBD1097','10.109.201.171','Reid'])
d.save()
d = DataRedis('rig',['OBD1098','10.109.201.172','Reid'])
d.save()
# print(DataRedis.queryAll('rig'))
# d = DataRedis('rig',['OBD1098','10.109.201.172','Reid'])
# d.delete()

print(DataRedis.queryAll('rig'))


    
