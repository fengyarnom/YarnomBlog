from flask import render_template,request,redirect, url_for,session
from initialize import app,db
from models.dbModels import *

from datetime import datetime
from enum import Enum

app.config["SECRET_KEY"] = "FengYarnomIsTheWebsiteAdmin"


# Router
@app.route("/")
def index():
    posts = Post.query.order_by(Post.id.desc()).all()

    return render_template('index.html',posts = posts)

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

@app.route("/new-post",methods=['POST', 'GET'])
def newPost():

    if request.method == "GET":
        title = request.args.get("title")
        content = request.args.get("content")
        post = Post(title=title, content=content, time=datetime.now())
        db.session.add(post)
        db.session.commit()
    return render_template('newPost.html')

@app.route("/admin",methods=['POST', 'GET'])
def admin():
    if session.get("loginName") and session.get("loginName") != "NULLNAME":
        return "<h1>Admin</h1>"
    else:
        return redirect(url_for('login'))

@app.route("/login_out")
def login_out():
    session["loginName"] = "NULLNAME"
    return redirect(url_for('index'))

# main function
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)