from flask import render_template,request,redirect, url_for,session
from initialize import app,db
from models.dbModels import *
import time
from datetime import datetime
from toolkit import *
from enum import Enum

app.config["SECRET_KEY"] = "FengYarnomIsTheWebsiteAdmin"


# Router
@app.route("/")
def index():
    try:
        userPermission = UserPermission()
        if userPermission.user_confirm():
            name = session.get("loginName")
        else:
            name = "登录"
        posts = Post.query.order_by(Post.id.desc()).all()
    except Exception as e:
        print(e)

    return render_template('index.html', posts=posts,name=name)

@app.route("/login",methods=['POST', 'GET'])
def login():
    #pass_state
    if session.get("loginName") and session.get("loginName") != "NULLNAME":
        return redirect(url_for('admin'))

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        for user in User.query.all():
            if username == user.username and password == user.password:
                session["loginName"] = username
                return redirect(url_for('admin'))
            else:
                session["loginName"] = "NULLNAME"
                state = 2
    else:
        state = 0

    return render_template('login.html',state = state)

@app.route("/admin/new-post",methods=['POST', 'GET'])
def newPost():
    # db.create_all()
    # db.session.commit()
    userPermission = UserPermission()

    if userPermission.user_confirm():
        if request.args.get("title") is not None:
            title = request.args.get("title")
            content = request.args.get("content")
            pid = time.strftime("%Y%m%d%H%M%S", time.localtime())
            post = Post(title=title, content=content, time=datetime.now(),pid=pid,isTop=0,archiveClass="Test")
            db.session.add(post)
            db.session.commit()
        return render_template('newPost.html')
    else:
        return redirect(url_for('login'))

@app.route("/admin",methods=['POST', 'GET'])
def admin():
    userPermission = UserPermission()

    if userPermission.user_confirm():
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

@app.route("/login_out")
def login_out():
    userPermission = UserPermission()
    userPermission.user_login_out()

    return redirect(url_for('index'))

@app.route("/post/<pid>")
def post(pid):
    post = Post.query.filter_by(pid=pid).first()
    return render_template('post.html',post=post)

# main function
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)