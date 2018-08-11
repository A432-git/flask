from redisworks import Root
class DataRedis2():
    root = Root(host='localhost')
    def __init__(self,dataName,_item):
        
        self.dataName = dataName
        self.redisFormat = "{}.{}".format(dataName,_item[0])
        self.content = _item
        # print(type(self.content))
        # self.__dict__.update(_item)
    
    def save(self):
        list = DataRedis2.root[self.dataName]
        print("adding {}...".format(self.content[0]))
        if(self.content not in list):
            list.append(self.content)
        else:
            index = list.index(['OBD1098','5400','david'])
            list[index] = ['OBD1098','5401','cherry']  
        DataRedis2.root[self.dataName] = list            
        # DataRedis2.root[self.dataName][self.content[0]] = self.content

        
    def delete(self):
        list = DataRedis2.root[self.dataName]
        print("deleting {}...".format(self.content[0]))
        if(self.content  in list):
            list.remove(self.content)  
            DataRedis2.root[self.dataName] = list        
    
    @staticmethod        
    def queryAll(dataName):
        
        return DataRedis2.root[dataName]
    
    @staticmethod        
    def initializationRedis(dataName,dataArray):
        
        DataRedis2.root[dataName]=dataArray

# dataArray = [[]]
# DataRedis2.initializationRedis('rig',dataArray)
# for i in range(100):
    # d = DataRedis2('rig',['OBD10{}'.format(i),'10.109.201.171','Reid'])
    # d.save()

# print(DataRedis2.queryAll('rig'))

# d = DataRedis2('rig',['OBD1098','5401','cherry'])
# d.delete()
# print(DataRedis2.queryAll('rig'))



    
