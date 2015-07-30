__author__ = 'fyl'

import hashlib
from app.models import User
from app import db
username = "alan"
passw = "alan"
password = hashlib.sha1(passw).hexdigest()
user = User(username=username,password=password)
db.session.add(user)
db.session.commit()