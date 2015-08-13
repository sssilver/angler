import flask.ext.login

import rod.model.staff


login_manager = flask.ext.login.LoginManager()


@login_manager.user_loader
def load_user(staff_id):
    return rod.model.staff.Staff.query.get(staff_id)
