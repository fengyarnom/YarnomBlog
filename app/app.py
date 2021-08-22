from flask import render_template,request,redirect, url_for
from datetime import datetime
import time

from initialize import *
from models.db.dbModels import *
from toolkit import *



# Router
@app.route("/",methods=['POST','GET'])
def index():
    posts = Post.query.order_by(Post.id.desc()).all()

    return render_template('index.html', posts=posts, username=session.get("username"))


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
            if request.form.get("title") is not None:
                title = request.form.get("title")
                content = request.form.get("content")
                pid = time.strftime("%Y%m%d%H%M%S", time.localtime())

                post = Post(title=title, content=content, time=datetime.now(), pid=pid, isTop=0, archiveClass="Test")
                db.session.add(post)
                db.session.commit()

            return render_template('newPost.html',username=session.get("username"))
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

@app.route("/admin",methods=['POST', 'GET'])
def admin():
    try:
        if user_action.getUserConfirm():
            return render_template('admin.html')
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

@app.route("/archive")
def archive():
    return render_template('archive.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)