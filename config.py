__author__ = 'fyl'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:yaolin878@localhost:3306/testflaskblog'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'fualan@foxmail.com'

PER_PAGE = 10