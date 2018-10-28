#!/usr/bin/env python
# encoding: utf-8


"""
@version: 0.1
@author: Yang Reid
@license: Apache Licence 
@contact: yangtao584@126.com
@site: https://github.com/yangr5/python
@software: PyCharm Community Edition
@file: sqlite_test.py
@time: 2018/8/23 9:43
"""

import sqlite3

conn = sqlite3.connect('labmangement.sqlite3')


def createTable():
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE work
           (id INTEGER PRIMARY KEY     NOT NULL,
           name           TEXT    NOT NULL,
           ar_found            INT     NOT NULL,
           ar_fix            INT     NOT NULL,
           script            INT     NOT NULL,
           cases            INT     NOT NULL,
           version            INT     NOT NULL);''')
    conn.commit()
    conn.close()
    print("Table created successfully")


def insertData():
    c = conn.cursor()
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
    conn.commit()
    conn.close()
    print( "Records created successfully")


def selectData():
    c = conn.cursor()
    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
       print ("ID = ", row[0])
       print ("NAME = ", row[1])
       print ("ADDRESS = ", row[2])
       print ("SALARY = ", row[3], "\n")

    conn.commit()
    conn.close()
    print ("Operation select done successfully")


if __name__ == "__main__":
    print ('This is main of module')
    createTable()


