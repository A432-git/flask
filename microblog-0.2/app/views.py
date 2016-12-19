from flask import render_template
from app import app
import xlrd
book = xlrd.open_workbook("test.xlsx")
@app.route('/')
@app.route('/array')
def array():
    user = {'nickname': 'Miguel'}
    sh = book.sheet_by_name("Sheet1")
    num_rows = sh.nrows
    posts=[]
    for curr_row in range(num_rows):
        post={}
        
        row = sh.row_values(curr_row)
        print('row%s is %s' %(curr_row,row))
        for curr_row in range(num_rows):
            post={}
            row = sh.row_values(curr_row)
            print('row%s is %s' %(curr_row,row))
            post['author']=row[0]
            post['body']=row[1]
            posts.append(post)
        
    return render_template("array.html",title = 'Home',user = user,posts = posts )
@app.route('/array2')
def array2():
    user = {'nickname': 'Miguel'}
    sh = book.sheet_by_name("Sheet2")
    num_rows = sh.nrows
    posts=[]
    head={}
    for curr_row in range(num_rows):
        post={}
        
        row = sh.row_values(curr_row)
        print('row%s is %s' %(curr_row,row))
        if(curr_row !=0):
            post['subject']=row[0]
            post['score']=row[1]
            posts.append(post)
        else:
            head['subject'] = row[0]
            head['score'] = row[1]
            print(head)
    return render_template("array2.html",title = 'Home',user = user,posts = posts,head=head  )
