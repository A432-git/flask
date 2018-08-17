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
        list = DataRedis2.root[self.dataName]['contents']
        list_name = [it[0] for it in list]
        # print(list)
        if(self.content[0] not in list_name):
            print("adding {}...".format(self.content[0]))
            list.append(self.content)
        else:
            print("updating {}...".format(self.content[0]))
            index = list_name.index(self.content[0])
            list[index] = self.content
        post = {'heads':DataRedis2.root[self.dataName]['heads'],'contents':list}          
        DataRedis2.root[self.dataName] = post

        
    def delete(self):
        list = DataRedis2.root[self.dataName]['contents']
        
        if(self.content  in list):
            print("deleting {}...".format(self.content[0]))
            list.remove(self.content) 
            post = {'heads':DataRedis2.root[self.dataName]['heads'],'contents':list}            
            DataRedis2.root[self.dataName] = post        
    
    @staticmethod        
    def queryAll(dataName,part = 'contents'):
        
        return DataRedis2.root[dataName][part]
    
    @staticmethod        
    def initializationRedis(dataName,dataKey,dataArray):
        
        DataRedis2.root[dataName]={'heads':dataKey,'contents':dataArray}

# dataArray = [[]]
# DataRedis2.initializationRedis('rig',dataArray)
# for i in range(100):
    # d = DataRedis2('rig',['OBD10{}'.format(i),'10.109.201.171','Reid'])
    # d.save()

# print(DataRedis2.queryAll('Array'))

# d = DataRedis2('Array',["JF-D1012", "VNX2 5400", "10.109.226.252", "10.109.226.175", "10.109.226.176", "Luo, Heng", "Dai, David", "Liu, Kai"])
# d.save()
# print(DataRedis2.queryAll('Array'))
# print(DataRedis2.queryAll('rig'))



    
