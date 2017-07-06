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
def initData():
    book = xlrd.open_workbook(DATA)
    sheetNames = book.sheet_names()

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
    return render_template("Home.html")

@app.route('/array')
def array():
    return render_template("data.html",posts = getData(sheetName = "Array"))

@app.route('/host')
def host():
    return render_template("data.html",posts = getData(sheetName = "Host"))

@app.route('/virtualization')
def virtualization():
    return render_template("data.html",posts = getData(sheetName = "Virtualization"))

@app.route('/falcon 404 IP assignment')
def falconIPAssignment():
    return render_template("data.html",posts = getData(sheetName = "Falcon 404 IP assignment"))
    
@app.route('/rockies')
def rockies():
    return render_template("data.html",posts = getData(sheetName = "Rockies"))
    
    
@app.route('/sanblaze')
def sanblaze():
    return render_template("data.html",posts = getData(sheetName = "Sanblaze"))

    
@app.route('/service')
def service():
    return render_template("data.html",posts = getData(sheetName = "Service"))    

@app.route('/daily tool')
def dailyTool():
    return render_template("data.html",posts = getData(sheetName = "Daily tool"))
    
@app.route('/special setup')
def specialSetup():
    return render_template("data.html",posts = getData(sheetName = "Special setup"))
    
@app.route('/standard tb')
def standardTB():
    return render_template("data.html",posts = getData(sheetName = "Standard TB"))
    
@app.route('/default configuration')
def defaultConfig():
    return render_template("data.html",posts = getData(sheetName = "Default configuration"))

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
