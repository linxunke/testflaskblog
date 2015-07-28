__author__ = 'fyl'

from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = "alan"
    return render_template("blog/index.html",title = 'Home',user = user)
