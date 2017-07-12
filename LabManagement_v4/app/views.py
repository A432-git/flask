import os
from flask import Flask, request,jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
import json
UPLOAD_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)),'Uploads')
DATA = os.path.join(UPLOAD_FOLDER,'data.xlsx')
JSON = os.path.join(UPLOAD_FOLDER,'data.json')
# allPages = {}

def loadJson(sheetName):
    with open(JSON, 'r') as f:
        data = json.load(f)
        return data[sheetName]

def getHeads(sheetName):
    sheet = loadJson(sheetName)
    return sheet['heads']

def getBody(sheetName):
    sheet = loadJson(sheetName)
    return sheet['body']
    
def jsonToFile(data):
    with open(JSON, 'w') as f:
        json.dump(data, f)

def getSheetNames():
    book = xlrd.open_workbook(DATA)
    sheetNames = book.sheet_names()
    return sheetNames
def initData():
    allPages = {}
    book = xlrd.open_workbook(DATA)
    sheetNames = book.sheet_names()
    allPages['keys']= sheetNames
    for sheetName in sheetNames:        
        sh = book.sheet_by_name(sheetName)
        num_rows = sh.nrows
        num_cols = sh.ncols
        num_rows = sh.nrows    
        posts={}
        posts['body']=[]
        posts['heads']=[]
        posts['title']=sheetName
        for curr_row in range(num_rows):
            post={}
            
            row = sh.row_values(curr_row)
            if(curr_row !=0):
                # post = dict(zip(heads,row))
                posts['body'].append(row)
                
            else:
                heads=row
                posts['heads'] = row
        allPages[sheetName] = posts
    jsonToFile(allPages)



@app.route('/data/Home')
def home():
    
    return render_template("Home.html",links=getSheetNames())

@app.route('/')
@app.route('/Main')
def main():
    initData()
    return render_template("main.html",links=getSheetNames())

    
@app.route('/data/<name>')
def data(name):
    return render_template("data.html",links=getSheetNames(),heads = getHeads(name),title = name )

@app.route('/ajax/<name>')
def ajaxJson(name):
        return jsonify(data =getBody(name))

              
@app.route('/manageByReid')
def manageByReid():
    return render_template("Manage.html",links=getSheetNames())
 
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('manage.html')
    elif request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename) 
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        initData()
        return render_template("main.html",links=getSheetNames())
