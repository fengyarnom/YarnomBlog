from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from toolkit import *
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
app.config["SECRET_KEY"] = "FengYarnomIsTheWebsiteAdmin"
db = SQLAlchemy(app)

user_action = UserAction()

def isInit():
    if os.path.isfile('app.db'):
        return True
    else:
        return False
