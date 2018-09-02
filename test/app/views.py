import os
from flask import Flask, request,jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd





@app.route('/')
@app.route('/datatable')
def home():
    return render_template("datatable.html")
    



