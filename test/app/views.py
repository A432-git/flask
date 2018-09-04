import os
from flask import Flask, request,jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
import xlrd
import time




@app.route('/')
@app.route('/datatable')
def home():
    return render_template("datatable.html")

@app.route('/test')
def test():
    return render_template("ajax_loading.html")


@app.route('/example', methods=['GET', 'POST'])
def example():
    time.sleep(1)
    old_content = request.form.get('old')
    print(f"{old_content}")
    return "I am ajax!"



