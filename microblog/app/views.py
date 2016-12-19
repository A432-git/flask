from flask import render_template
from app import app
import xlrd
book = xlrd.open_workbook("test.xlsx")

@app.route('/')
@app.route('/home')
def home():
    return render_template("Home.html",title = 'home',)

@app.route('/array')
def array():
    sh = book.sheet_by_name("Sheet1")
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
    return render_template("array.html",title = 'array',posts = posts)

@app.route('/score')
def score():
    sh = book.sheet_by_name("Sheet2")
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
    return render_template("array.html",title = 'score',posts = posts)