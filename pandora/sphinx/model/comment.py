from model import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id              = db.Column(db.Integer, primary_key=True)
    repliee_id      = db.Column(db.Integer, index=True)
    time            = db.Column(db.DateTime)
    content         = db.Column(db.Text)

    replier_id      = db.Column(db.Integer, db.ForeignKey('users.id'))
    video_id        = db.Column(db.Integer, db.ForeignKey('videos.id'))

    def __repr__(self):
        return '<Comment %r>' % self.content