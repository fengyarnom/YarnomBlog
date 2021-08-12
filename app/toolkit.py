from flask import session

class UserPermission:
    def user_confirm(self):
        if session.get("loginName") and session.get("loginName") != "NULLNAME":
            return True
        else:
            return False

    def user_login_out(self):
        session["loginName"] = "NULLNAME"
        return 0
