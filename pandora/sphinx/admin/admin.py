from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from model import db, follow_table
from model import user, video, notification, follow, comment

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

        
def init_admin(app):
    admin = Admin(app, url='/admin', endpoint='admin', name = "adminapp")
    admin.add_view(ModelView(video.Video, db.session ,endpoint='mv_video'))
    admin.add_view(ModelView(user.User, db.session ,endpoint='mv_user'))
    admin.add_view(ModelView(notification.Notification, db.session ,endpoint='mv_notification'))
    admin.add_view(ModelView(follow.Follow, db.session ,endpoint='mv_follow'))
    admin.add_view(ModelView(comment.Comment, db.session ,endpoint='mv_comment'))
    #admin.add_view(ModelView(follow_table, db.session ,endpoint='mv_follow_table'))
    
    return admin