
from initialize import db

Base = db.Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.Date, nullable=False)
    pid = db.Column(db.String(128), nullable=False)
    isTop = db.Column(db.Integer, nullable=True)
    tag = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return '<Post %r>' % self.title


class ArchiveClass(db.Model):
    name = db.Column(db.String(256), unique=True, primary_key=True, nullable=False)

    def __repr__(self):
        return '<ArchiveClass %r>' % self.name


class Note(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.Date, nullable=False)
    pid = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Note %r>' % self.title
