import os
from flask import Flask, request,jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
import json
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
    
@app.route('/g2_2')
def g2_2():
    return render_template("g2_2.html")

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