from flask import session
from toolkit import *

class UserAction:
    def getUserConfirm(self):
        if session.get("username") is not None:
            return True
        else:
            return False

    def setUserSignOut(self):
        session["loginName"] = "NULLNAME"
        return 0

    def setUserLogin(self,table,username,password):
        res = table.query.filter_by(username=username,password=password).first()
        if res is not None:
            session["username"] = username
            return "AccountCorrect"
        else:
            return "AccountError"