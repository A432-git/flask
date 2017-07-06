import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
UPLOAD_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)),'Uploads')
DATA = os.path.join(UPLOAD_FOLDER,'data.xlsx')
allPages = {}
def initData():
    book = xlrd.open_workbook(DATA)
    sheetNames = book.sheet_names()
    allPages['keys'] = sheetNames


@app.route('/')
@app.route('/home/')
def home():
    initData()
    return render_template("Home.html",links=allPages['keys'])

