__author__ = 'fyl'

from flask import Flask

app = Flask(__name__)

from app.blog import views