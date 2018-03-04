import os
from flask import Flask, request,jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
import json
from .work import Work
UPLOAD_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)),'Uploads')
DATA = os.path.join(UPLOAD_FOLDER,'data.xlsx')
allPages = {}
def initData():
    book = xlrd.open_workbook(DATA)
    sheetNames = book.sheet_names()
    allPages['keys'] = sheetNames

@app.route('/g2')
def g2():
    return render_template("base_bak.html")
 

@app.route('/g2_db')
def g2_db():
    return render_template("g2.html")
 
@app.route('/g2_2')
def g2_2():
    return render_template("g2_2.html")
    

    
@app.route('/g2_3')
def g2_3():
    return render_template("g2_3.html")

@app.route('/g2_4')
def g2_4():
    return render_template("g2_4.html")
    
@app.route('/')
@app.route('/home/')
def home():
    #initData()
    return render_template("1.html")
    

    
@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        body = request.form['body']
        json_data = json.loads(body)
        length=json_data.pop('length')
        length1=len(json_data['0'])
        values = list(json_data.values())
        
        n = [request.form.get(x, 0, type=float) for x in {'n1','n2','n3'}]
        return jsonify(max=max(n), min=min(n),body = body,length=length,length1=length1,dt=[1,2,3])
    else:
        return render_template('1.html')

@app.route('/ar')
def data():
    with open('ar.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/ar2')
def data2():
    data = [
    { "month": "Jan", "Tokyo": 7.0, "London": 3.9 },
    { "month": "Feb", "Tokyo": 6.9, "London": 4.2 },
    { "month": "Mar", "Tokyo": 9.5, "London": 5.7 },
    { "month": "Apr", "Tokyo": 14.5, "London": 8.5 },
    { "month": "May", "Tokyo": 18.4, "London": 11.9 },
    { "month": "Jun", "Tokyo": 21.5, "London": 15.2 },
    { "month": "Jul", "Tokyo": 25.2, "London": 17.0 },
    { "month": "Aug", "Tokyo": 26.5, "London": 16.6 },
    { "month": "Sep", "Tokyo": 23.3, "London": 14.2 },
    { "month": "Oct", "Tokyo": 18.3, "London": 10.3 },
    { "month": "Nov", "Tokyo": 13.9, "London": 6.6 },
    { "month": "Dec", "Tokyo": 9.6, "London": 4.8 }
  ]
    return jsonify(data)
    
    
@app.route('/ar3')
def data3():
    data =[
    { 'name':'London', 'Jan.': 18.9, 'Feb.': 28.8, 'Mar.' :39.3, 'Apr.': 81.4, 'May': 47, 'Jun.': 20.3, 'Jul.': 24, 'Aug.': 35.6 },
    { 'name':'Berlin', 'Jan.': 12.4, 'Feb.': 23.2, 'Mar.' :34.5, 'Apr.': 99.7, 'May': 52.6, 'Jun.': 35.5, 'Jul.': 37.4, 'Aug.': 42.4}
  ]
    return jsonify(data)
    
@app.route('/ar4')
def data4():
    # data=[{'ar_found': 100, 'script': 23, 'name': 'reid', 'ar_fix': 122, 'case': 20}, {'ar_found': 90, 'script': 120, 'name': 'david', 'ar_fix': 102, 'case': 30}, {'ar_found': 80, 'script': 30, 'name': 'cherry', 'ar_fix': 80, 'case': 40}, {'ar_found': 80, 'script': 50, 'name': 'jia', 'ar_fix': 78, 'case': 86}, {'ar_found': 90, 'script': 29, 'name': 'leon', 'ar_fix': 38, 'case': 130}, {'ar_found': 30, 'script': 100, 'name': 'bonn', 'ar_fix': 99, 'case': 20}, {'ar_found': 30, 'script': 29, 'name': 'jesssie', 'ar_fix': 60, 'case': 110}, {'ar_found': 88, 'script': 50, 'name': 'jennifer', 'ar_fix': 40, 'case': 80}]
    data=[]
    works = Work.query.all()
    test = works[0]
    testdict= test.getJson()
    fields = list(testdict.keys())
    fields.remove('name')
    for work in works:   
        data.append(work.getJson())
       
    return jsonify(data = data,fields = fields)
