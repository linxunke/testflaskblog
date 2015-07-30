__author__ = 'fyl'
#coding:utf-8
from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = "alan"
    return render_template("blog/index.html",title = 'Home',user = user)

@app.route('/about')
def about():
    return render_template("blog/about.html")