__author__ = 'fyl'

from app import db
from datetime import datetime
from config import PER_PAGE

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __str__(self):
        return '%s' % (self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def login_check(cls,username,password):
        user = cls.query.filter(User.username==username).filter(User.password==password).first()
        if not user:return  None
        return user




article_tag_table = db.Table('article_tags',db.Model.metadata,db.Column('article_id',db.Integer,db.ForeignKey('articles.id')),db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True)

    def __init__(self,name):
        self.name = name

    @classmethod
    def all_page(cls,page):
        return cls.query.order_by(cls.id.desc()).paginate(page, PER_PAGE, False)

    @classmethod
    def search_page(cls,page,keyword):
        return cls.query.filter(cls.name.ilike('%%%s%%' % keyword)).paginate(page, PER_PAGE, False)

    def __str__(self):
        return '%s' % (self.name)



class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True)
    description = db.Column(db.Text())
    articles = db.relationship('Article',backref='categorys',lazy='dynamic')

    def __init__(self,name,description):
        self.name = name
        self.description = description

    def __str__(self):
        return '%s' % (self.name)

    @classmethod
    def check_by_name(cls,keyword):
        return cls.query.filter_by(name=keyword).first()

    @classmethod
    def search_page(cls,page,keyword):
        return cls.query.filter(cls.name.ilike('%%%s%%' % keyword)).paginate(page, PER_PAGE, False)

    @classmethod
    def all_page(cls,page):
         return  cls.query.order_by(cls.id.desc()).paginate(page, PER_PAGE, False)



class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    context = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    view_count = db.Column(db.Integer,default=0)
    category_id = db.Column(db.Integer,db.ForeignKey('categorys.id'))
    tags = db.relationship('Tag',secondary=article_tag_table,backref='articles')


    def __init__(self,title,context,created_at,view_count,category_id,tags):
        self.title = title
        self.context = context
        self.view_count = view_count
        self.category_id = category_id
        self.tags = tags

        if created_at is None:
            self.created_at = datetime.utcnow()
        else:
            self.created_at = created_at

    def __str__(self):
        return '%s' % (self.title)

