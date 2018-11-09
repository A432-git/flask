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

    if force == 0:
        if root.lab and root.tb.keys:
            pass
        else:
            readExcelToRedis()
            root.tb.keys = ['test']
            root.tb.device = ['OB-D1097']
            root.tb.connection = ['sync', 'async']
    else:
        readExcelToRedis()


@app.before_first_request
def before_first_request():
    init()


@app.route('/')
@app.route('/home/')
def home():
    return render_template("Main.html",labItems=root.lab['keys'],workItems=root.work['keys'])
    

@app.route('/ts/<obj>')
def external_ts(obj):
    if obj == 'testbed':
        # root.tb.keys = ['test']
        # root.tb.device = ['OB-D1097']
        # root.tb.connection = ['sync','async']
        return render_template('testbed' + ".html", devices=root.tb.device,connections=root.tb.connection,testbed_type=root.tb.keys)
    else:
        return render_template(obj + ".html")


@app.route('/ts/tb/device/<operate>/<device_name>')
def operate_device(operate,device_name):
    device_list = []
    for device in root.tb.device:
        device_list.append(device)
    if operate == 'add':
        device_list.append(device_name)

    else:
        device_list.remove(device_name)
    root.tb.device = device_list
    return jsonify(result = [])


@app.route('/ts/tb/connection/<operate>/<connection_name>')
def operate_relation(operate,connection_name):
    connection_list = []
    for relation in root.tb.connection:
        connection_list.append(relation)
    if operate == 'add':
        connection_list.append(connection_name)
    else:
        connection_list.remove(connection_name)
    root.tb.connection = connection_list
    return jsonify(result = [])


@app.route('/ts/tb/<tb_name>')
def getTB(tb_name):
    key = f'tb.{tb_name}'
    print(root[key])
    if root[key]:
        return jsonify(relation=root[key])
    else:
        return jsonify(relation=[])


@app.route('/ts/tb/<operation>/<tb_name>',methods=['GET', 'POST'])
def operate_tb(operation,tb_name):
    content = json.loads(request.form.get('content'))
    if operation == 'update':
        key = f'tb.{tb_name}'
        root[key] = content
        testbed_type = []
        for it in root.tb.keys:
            testbed_type.append(it)
        testbed_type.append(tb_name)
        print(f'add new {tb_name}')
        testbed_type = list(set(testbed_type))
        root.tb.keys = testbed_type
    res = {}
    res['code'] = 0
    return jsonify(res)



@app.route('/data_excel/<cycle_name>')
def data_excel(cycle_name):
    return render_template("data_excel.html",heads = root.work[cycle_name]['heads'],title = cycle_name)
    

@app.route('/dataExcel/<cycle_name>')
def dataExcel(cycle_name):
    return jsonify(root.work[cycle_name])


@app.route('/dataExcelArray/<cycle_name>')
def dataExcelArray(cycle_name):
    return jsonify(data = root.work[cycle_name]['body_arr'])


@app.route('/data/<name>')
def dataLab(name):
    if(name=='Home'):
        return render_template("Home.html")
    else:
        return render_template("data.html",heads = root.lab[name]['heads'],title = name)


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
        # return jsonify(status='succeed')
        return render_template("Home.html")