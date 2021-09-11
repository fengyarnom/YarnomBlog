
from flask import render_template,request,redirect, url_for
from datetime import datetime
import time
from markupsafe import Markup
from sqlalchemy import func

from initialize import *
from db_models import *
from toolkit import *
from web_config import *


# Router
@app.route("/",methods=['POST','GET'])
def index():
    try:
        while(not isInit()):
            if request.method == "POST":
                if request.form.get("password") is not None:
                    username = request.form.get("username")
                    password = request.form.get("password")
                    db.create_all()
                    admin = User(username=username,password=password)
                    db.session.add(admin)
                    db.session.commit()
                    break
            return render_template('getStart.html')

        tops = Post.query.order_by(Post.id.desc()).filter_by(isTop=1).all()
        posts = Post.query.order_by(Post.id.desc()).filter_by(isTop=0).limit(5).all()
        tags = ArchiveClass.query.limit(3).all()
        notes = Note.query.all()
        return render_template('index.html',
                               posts= posts,
                               tops= tops,
                               tags = tags ,
                               notes = notes)
    except Exception as e:
        print(e)




@app.route("/login",methods=['POST','GET'])
def login():
    try:
        if user_action.getUserConfirm():
            return redirect(url_for('admin'))
        else:
            if request.method == "POST":
                username = request.form.get('username')
                password = request.form.get('password')
                account_state = user_action.setUserLogin(table=User,username=username,password=password)
                if account_state == "AccountCorrect":
                    return redirect(url_for('admin'))
                else:
                    return render_template('login.html',account_state = account_state,username=session.get("username"))
    except Exception as e:
        print(e)

    return render_template('login.html',account_state = "AccountSignOut",username=session.get("username"))

@app.route("/new-post",methods=['POST', 'GET'])
def newPost():
    try:
        if user_action.getUserConfirm():
            archiveClass = ArchiveClass.query.all()

            if request.form.get("title") is not None:
                title = request.form.get("title")
                content = request.form.get("content").strip()
                pid = time.strftime("%Y%m%d%H%M%S", time.localtime())
                tag = request.form.get("tag").strip()
                isTop = request.form.get("isTop")

                if(len(tag) == 0):
                    tag = "#"

                if(request.form.get("post_class") == 'post'):
                    req = Post(title=title, content=content, time=datetime.now(), pid=pid, isTop=isTop, tag=tag)
                else:
                    req = Note(title=title, content=content, time=datetime.now(), pid=pid)

                if(len(tag) != 0 and ArchiveClass.query.filter_by(name=tag).first() is None):
                    req2 = ArchiveClass(name=tag)
                    db.session.add(req2)

                db.session.add(req)
                db.session.commit()

            return render_template('newPost.html',archiveClass=archiveClass)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
@app.route("/uploadImg",methods=['POST'])
def uploadImg():
    try:
        if user_action.getUserConfirm():
            basedir = os.path.abspath(os.path.dirname(__file__))
            img = request.files.get('pic')
            path=basedir+'/static/upload/imgs/'
            img_path=path+img.filename
            img.save(img_path)
            return img.filename
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
@app.route("/modifyPost/<pid>",methods=['POST', 'GET'])
def modifyPost(pid):
    try:
        if user_action.getUserConfirm():
            archiveClass = ArchiveClass.query.all()
            post = Post.query.filter_by(pid = pid).first()
            if request.form.get("title") is not None:
                post.title = request.form.get("title")
                post.content = request.form.get("content")

                if(len(request.form.get("tag").strip()) != 0):
                    post.tag = request.form.get("tag").strip()

                post.isTop = request.form.get("isTop")
                if(len(post.tag) != 0 and ArchiveClass.query.filter_by(name=post.tag).first() is None):
                    req2 = ArchiveClass(name=post.tag)
                    db.session.add(req2)
                db.session.commit()
            return render_template('modifyPost.html',archiveClass=archiveClass,post=post)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
@app.route("/deletePost",methods=['POST', 'GET'])
def deletePost():
    try:
        if user_action.getUserConfirm():
            if request.form.get("deletePid") is not None:
                pid = request.form.get("deletePid")
                post = Post.query.filter_by(pid = pid).first()
                db.session.delete(post)
                db.session.commit()
            return ":)"

        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

@app.route("/deleteNote",methods=['POST', 'GET'])
def deleteNotes():
    try:
        if user_action.getUserConfirm():
            if request.form.get("deletePid") is not None:
                pid = request.form.get("deletePid")
                notes = Note.query.filter_by(pid = pid).first()
                db.session.delete(notes)
                db.session.commit()
            return ":)"

        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
@app.route("/admin",methods=['POST', 'GET'])
def admin():
    try:
        if user_action.getUserConfirm():
            counts = dict();
            counts["post"] =db.session.query(func.count(Post.id)).scalar()
            counts["user"] =db.session.query(func.count(User.id)).scalar()
            counts["note"] =db.session.query(func.count(Note.id)).scalar()

            posts = Post.query.order_by(Post.id.desc()).all()
            notes = Note.query.order_by(Note.id.desc()).all()
            users = User.query.order_by(User.id).all()

            return render_template('admin.html',counts=counts,posts=posts,notes=notes,users=users)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

@app.route("/admin/tags",methods=['POST', 'GET'])
def admin_tags():
    try:
        if user_action.getUserConfirm():
            tags = ArchiveClass.query.all()
            return render_template('admin-tags.html',tags=tags)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
@app.route("/admin/notes",methods=['POST', 'GET'])
def admin_notes():
    try:
        if user_action.getUserConfirm():
            notes = Note.query.all()
            return render_template('admin-notes.html',notes=notes)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

@app.route("/login_out")
def login_out():
    userPermission = UserPermission()
    userPermission.user_login_out()

    return redirect(url_for('index'))

@app.route("/post/<pid>")
def post(pid):
    post = Post.query.filter_by(pid=pid).first()
    return render_template('post.html',post=post)

@app.route("/archive",methods=['POST', 'GET'])
def archive():
    if request.args.get("year"):
        year = int(request.args.get("year"))
    else:
        year = datetime.now().year

    posts = Post.query.filter(
        (Post.time >= datetime(year, 1, 1)) & (Post.time <= datetime(year, 12, 31))
    ).all()

    return render_template('archive.html',time=datetime.now(),posts=posts)

@app.route("/archive/tags/<tag>",methods=['POST', 'GET'])
def archive_tags(tag):
    if request.args.get("year"):
        year = int(request.args.get("year"))
    else:
        year = datetime.now().year

    posts = Post.query.filter(
        (Post.time >= datetime(year, 1, 1)) & (Post.time <= datetime(year, 12, 31)) &(Post.tag == tag)
    ).all()

    return render_template('tags.html',time=datetime.now(),posts=posts,tag=tag)

@app.route("/demo",methods=['POST', 'GET'])
def demo():

    return render_template('demo.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
