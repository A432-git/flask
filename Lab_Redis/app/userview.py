import os
from flask import Flask, session,request,jsonify, render_template,g, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
import json
from redisworks import Root
import configparser 
UPLOAD_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)),'Uploads')
INI = os.path.join(UPLOAD_FOLDER,'test.ini')
config = configparser.ConfigParser()
config.read(INI)

root = Root(host=config['DEFAULT']['redis_ip'])

def readExcelToRedis():
    for section in config.sections():
        excelItem = os.path.join(UPLOAD_FOLDER,config[section]['file'])
        redisKey = config[section]['redis_key']
        allPagesDict = {}
        book = xlrd.open_workbook(excelItem)
        sheetNames = book.sheet_names()
        allPagesDict['keys'] = sheetNames
        for sheetName in sheetNames:        
            sh = book.sheet_by_name(sheetName)
            num_rows = sh.nrows
            num_cols = sh.ncols  
            posts={}
            posts['body']=[]
            posts['body_arr']=[]
            posts['heads']=[]
            posts['title']=sheetName
            
            for curr_row in range(num_rows):  
                post={} 
                row = sh.row_values(curr_row)
                if(curr_row !=0):
                    post = dict(zip(heads,row))
                    posts['body'].append(post)   
                    posts['body_arr'].append(row)
                else:
                    heads=row
                    posts['heads'] = row
            allPagesDict[sheetName] = posts
        root[redisKey] = allPagesDict
def init(force =0):
    if(force == 0):
        if(root.lab):
            pass
        else:
            readExcelToRedis()
    else:
        readExcelToRedis()
@app.before_first_request
def  before_first_request():
    init()

@app.route('/')
@app.route('/home/')
def home():
    return render_template("UserMain.html",labItems=root.lab['keys'],workItems=root.work['keys'])
 
    
@app.route('/userview/<name>')
def dataLab(name):

    if(name=='Home'):
        return render_template("Home.html")
    else:
        return render_template("data.html",heads = root.lab[name]['heads'],title = name)
  


@app.route('/ajax/<name>/<action>',methods=['GET','POST'])
def actionJson(name,action):
    heads = root.lab[name]['heads']
    values=[]
    # for it in heads:
        # values.append('hello')
        # print('+++++++++++')
    # data = zip(heads,values)
    data={'name':'reid'}
    if action == 'create':
        
        return jsonify(data)
    elif action == 'update':
    
        return jsonify(data)
    elif action == 'delete':
    
        print('--------------')
        return jsonify(data)
    else:
        return jsonify(data)    
    return jsonify(data)  
        
@app.route('/ajax/<name>')
def ajaxJson(name):
    return jsonify(data = root.lab[name]['body_arr'])
        
@app.route('/manageByReid')
def manageByReid():
    return render_template("Manage.html")
 
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('manage.html')
    elif request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename) 
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        init(force =1)
        return jsonify(status='succeed')
