from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Router
@app.route("/")
def index():
    dict = {
        'hello':'Hello'
    }
    return render_template('index.html',dict=dict)

@app.route("/login")
def login():
    return render_template('login.html')

# main function
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True,host='0.0.0.0',port=3000)