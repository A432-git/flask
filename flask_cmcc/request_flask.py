#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: yangtao
@contact:yangtao584@126.com
@version: 1.0.0
@license: Apache Licence
@file: request_flask.py
@time: 23/12/20 20:09
"""
import requests,json
import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

class ReportTCStatus:
    @staticmethod
    def f1(data):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        with requests.session() as s:
            r = s.post(url='http://localhost:5001/test',headers=headers,
                       data=json.dumps(data,cls=DateEncoder)
                       # json=data
                       )

            # res = requests.post(url=url, data=json.dumps(data))
            print(r.status_code,r.text)


if __name__ == '__main__':
    data = {
        "project": "project_1",
        "plan": "plan_1",
        "tc_id":"test_193",
        "result":'Blocked',
        "bug":"bug_01",
        "logs":"""http://www.baidu.com""",
        "detail":"""XXXXXXXXXXXXXXXXXXXXXx,
        XXXXXXXXXXXXXXXXXXXXX
        XXXXXXXXXXXXXXXXXXXXX""",
        "execute_date":datetime.datetime.strptime("2020-12-23 20:01:00", '%Y-%m-%d %H:%M:%S'),
        "executor":"yangtao"
    }
    import time
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    b = datetime.datetime.now()
    print(type(b),b)
    s = '1978-01-01 12:00:00'  # type(str)
    new_time = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    print(type(new_time))
    ReportTCStatus.f1(data)
