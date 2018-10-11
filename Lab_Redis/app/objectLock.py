#!/usr/bin/env python
# _*_ coding:UTF-8


import threading
import time
import random


class ObjectLock():
    '''对象锁，在一个对象上加锁或释放锁，实现对一个对象访问的串行化'''

    def __init__(self):
        self.cond = threading.Condition()
        self.objSet = set()

    def lock(self, obj):
        '''在obj上加锁'''

        self.cond.acquire()
        while obj in self.objSet:
            self.cond.wait()
        self.objSet.add(obj)
        self.cond.release()

    def unLock(self, obj):
        '''释放obj上的锁'''

        self.cond.acquire()
        self.objSet.remove(obj)
        self.cond.notifyAll()
        self.cond.release()



class MyThread(threading.Thread):

    def __init__(self, tid, oLock):
        threading.Thread.__init__(self)
        self.tid = tid
        self.oLock = oLock

    def run(self):
        while True:
            vol = random.randint(1, 3)
            self.oLock.lock(vol)
            print("thread %d: process %d begin" % (self.tid, vol))
            time.sleep(4)
            print("thread %d: process %d end" % (self.tid, vol))
            self.oLock.unLock(vol)


if __name__ == "__main__":
    oLock = ObjectLock()
    for i in range(10):
        t = MyThread(i, oLock)
        t.start()
