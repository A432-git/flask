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


@app.route('/example')
def example():
    time.sleep(3)
    return jsonify("I am ajax!")
    



