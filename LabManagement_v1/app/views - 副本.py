import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
# dirname=os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER =r'.\app\Uploads'
# DATA = r'.\app\Uploads\data.xlsx'
UPLOAD_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)),'Uploads')
DATA = os.path.join(UPLOAD_FOLDER,'data.xlsx')
allPages = {}
def getKeys():
    book = xlrd.open_workbook(DATA)
    sheetNames = book.sheet_names()
    return sheetNames
def initData():
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
        for curr_row in range(num_rows):
            post={}
            
            row = sh.row_values(curr_row)
            if(curr_row !=0):
                post = dict(zip(heads,row))
                posts['body'].append(post)
                
            else:
                heads=row
                posts['heads'] = row
        allPages[sheetName] = posts
def getData(sheetName):
    if(len(allPages.keys()) < 1):
        initData()
    return allPages[sheetName]
@app.route('/')
@app.route('/home/')
def home():
    return render_template("Home.html",links=getKeys())

@app.route('/Array')
def array():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Array"))

@app.route('/Host')
def host():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Host"))

@app.route('/Virtualization')
def virtualization():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Virtualization"))

@app.route('/Falcon 404 IP assignment')
def falconIPAssignment():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Falcon 404 IP assignment"))
    
@app.route('/Rockies')
def rockies():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Rockies"))
    
    
@app.route('/Sanblaze')
def sanblaze():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Sanblaze"))

    
@app.route('/Service')
def service():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Service"))    

@app.route('/Daily tool')
def dailyTool():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Daily tool"))
    
@app.route('/Special setup')
def specialSetup():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Special setup"))
    
@app.route('/Standard tb')
def standardTB():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Standard TB"))
    
@app.route('/Default configuration')
def defaultConfig():
    return render_template("data.html",links=getKeys(),posts = getData(sheetName = "Default configuration"))

@app.route('/manageByReid')
def manageByReid():
    return render_template("Manage.html",)
 
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('manage.html')
    elif request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename) 
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        initData()
        return render_template("data.html",posts = getData(sheetName = "Array"))
