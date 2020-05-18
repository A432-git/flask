#!/usr/bin/python
# encoding: utf-8
"""
@author: yangr5 
@contact: yangtao584@126.com
@version: 1.0
@license: Apache Licence
@file: redis_test.py
@time: 2019-09-03 15:10

这一行开始写关于本文件的说明与解释
"""
from redisworks import Root
import json

root = Root(host='18.221.249.189')

def main():
    # root.test = [1,2,3]
    with open('data.json') as json_file:
        data = json.load(json_file)
        # print(data)
        root.dm.array = data
    # print(root.test)
    for rig in root.dm.array:
        print(rig)


if __name__ == '__main__':
    main()

