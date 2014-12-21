from flask.ext.admin import Admin

def init_admin(app):
    admin = Admin(app)
    return admin