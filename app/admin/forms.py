__author__ = 'fyl'

from flask_wtf import Form
from wtforms import StringField,validators,PasswordField,BooleanField,TextAreaField,DateTimeField
from datetime import datetime

class LoginForm(Form):
    username = StringField('Name',[validators.required(), validators.length(max=200)])
    password = PasswordField('password',[validators.required(), validators.length(max=200)])
    rememberme = BooleanField('remember',default=False)


class CategoryForm(Form):
    name = StringField('name',[validators.required(), validators.length(max=200)])
    description = TextAreaField('descriptions',[validators.required()])

class TagForm(Form):
    name = StringField('name',[validators.required(), validators.length(max=200)])

class AritcleForm(Form):
    title = StringField('title',[validators.required(), validators.length(max=200)])
    context = TextAreaField('context',[validators.required()])
    created_at = DateTimeField('created_at',[validators.required()],default=datetime.now())
    view_count = StringField('view_count',[validators.required()],default=0)
