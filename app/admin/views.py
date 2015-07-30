__author__ = 'fyl'
#coding:utf-8
from app import app,login_manager,db
from app.models import User,Category,Article,Tag
from flask import render_template,redirect,flash,session,request,url_for
from flask.ext.login import login_user,logout_user,current_user,login_required
from app.admin.forms import LoginForm,CategoryForm,AritcleForm,TagForm
import  hashlib

@login_manager.user_loader
def load_user(userid):
    return  User.query.get(int(userid))

@app.route('/admin/',methods=['GET','POST'])
@app.route('/admin/login/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('admin'))

    form = LoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        passw = hashlib.sha1(password).hexdigest()
        user = User.login_check(username,passw)
        if user:
            login_user(user)
            return redirect(url_for('admin'))

    return render_template('admin/signin.html',form=form)

@app.route('/admin/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/index/')
@login_required
def admin():
    user = current_user
    return render_template("admin/admin.html",user=user)



#######  Blog  Article---Category####################


@app.route('/admin/addcategory/',methods=['GET','POST'])
@login_required
def add_category():
    categoryform = CategoryForm()

    if categoryform.validate_on_submit():
        category_name = request.form.get('name')
        category_description = request.form.get('description')
        if(category_name != None and category_description != None and category_name !="" and category_description != ""):
            category = Category.check_by_name(category_name)
            if(category is None):
                category = Category(name=category_name,description=category_description)
            else:
                flash("category:%s is already exit" % category)
            try:
                db.session.add(category)
                db.session.commit()
            except:
                flash("add_category Database error!")
                return render_template("admin/addcategory.html",categoryform=categoryform)
        return redirect(url_for('list_category'))
    return render_template("admin/addcategory.html",categoryform=categoryform)

@app.route('/admin/listcategory/',defaults={'page':1},methods=['GET','POST'])
@app.route('/admin/listcategory/page/<int:page>',methods=['GET','POST'])
@login_required
def list_category(page):
    category = Category.all_page(page)
    return render_template("admin/listcategory.html",category=category,keyword=None)

@app.route('/admin/searchcategory/',defaults={'keyword':None,'page':1},methods=['GET','POST'])
@app.route('/admin/searchcategory/<string:keyword>/<int:page>',methods=['GET','POST'])
@login_required
def search_category(page,keyword):
    if not keyword:
        keyword = request.form.get('keyword')

    if keyword == None or keyword == "":
        return redirect(url_for('list_category'))
    else:
        category = Category.search_page(page,keyword)
        return render_template("admin/listcategory.html",category=category,keyword=keyword)


@app.route('/admin/deletecategory/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    try:
        if not category.articles.all():
            db.session.delete(category)
            db.session.commit()
        else:
            flash("此category：%s关联着有articles,你必须删除完articles才能删除此category" % category.name)
            return redirect(url_for("list_category"))
    except:
        flash("delete_category Database error!")
        return redirect(url_for("list_category"))
    return redirect(url_for("list_category"))



@app.route('/admin/editcategory/<int:id>',methods=['GET','POST'])
@login_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first()
    categoryform = CategoryForm(name=category.name,description=category.description)
    if categoryform.validate_on_submit():
        category_name = request.form.get('name')
        category_description = request.form.get('description')
        try:
            Category.query.filter_by(id=id).update({Category.name:category_name,Category.description:category_description})
            db.session.commit()
        except:
            flash("edit_category Database error!")
            return render_template("admin/editcategory.html",categoryform=categoryform,category=category)
        return redirect(url_for("list_category"))
    return render_template("admin/editcategory.html",categoryform=categoryform,category=category)


#######  Blog  Article---Tag####################


@app.route('/admin/edittag/<int:id>',methods=['GET','POST'])
@login_required
def edit_tag(id):
    tag = Tag.query.filter_by(id=id).first()
    tagform = TagForm(name=tag.name)

    if tagform.validate_on_submit():
        tag_name = request.form.get('name')

        try:
            Tag.query.filter_by(id=id).update({Tag.name:tag_name})
            db.session.commit()
        except:
            flash("edit_tag Database error!")
            return render_template("admin/edittag.html",tagform=tagform,tag=tag)
        return redirect(url_for("list_tag"))
    return render_template("admin/edittag.html",tagform=tagform,tag=tag)

@app.route('/admin/addtag/',methods=['GET','POST'])
@login_required
def add_tag():
    tagform = TagForm()

    if tagform.validate_on_submit():
        tag_name = request.form.get('name')
        tag = Tag(name=tag_name)

        try:
            db.session.add(tag)
            db.session.commit()
        except:
            flash("add_tag Database error!")
            return render_template("admin/addtag.html",tagform=tagform)
        return redirect(url_for('list_tag'))
    return render_template("admin/addtag.html",tagform=tagform)

@app.route('/admin/searchtag/',defaults={'keyword':None,'page':1},methods=['GET','POST'])
@app.route('/admin/searchtag/<string:keyword>/<int:page>',methods=['GET','POST'])
@login_required
def search_tag(page,keyword):
    if not keyword:
        keyword = request.form.get('keyword')


    if keyword == None or keyword == "":
        return redirect(url_for('list_tag'))
    else:
        tag = Tag.search_page(page,keyword)
        return render_template("admin/listtag.html",tag=tag,keyword=keyword)


@app.route('/admin/deletetag/<int:id>')
@login_required
def delete_tag(id):
    tag = Tag.query.filter_by(id=id).first()
    try:
        if not tag.articles:
            db.session.delete(tag)
            db.session.commit()
        else:
            flash("delete_tag Database error!你必须删除完此标签下的所有articles才能删除此tag" )
    except:
        flash("delete_tag Database error!你必须删除完此标签下的所有articles才能删除此tag" )
        return redirect(url_for("list_tag"))
    return redirect(url_for("list_tag"))


@app.route('/admin/listtag/',defaults={'page':1},methods=['GET','POST'])
@app.route('/admin/listtag/page/<int:page>',methods=['GET','POST'])
@login_required
def list_tag(page):
    tag = Tag.all_page(page)
    return render_template("admin/listtag.html",tag=tag,keyword=None)