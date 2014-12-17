import datetime

from model import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id              = db.Column(db.Integer, primary_key=True)
    time            = db.Column(db.DateTime)
    content         = db.Column(db.Text)

    # backref as replier
    replier_id      = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    # backref as repliee
    repliee_id      = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    # backref as video
    video_id        = db.Column(db.Integer, db.ForeignKey('videos.id'), index=True)

    def __repr__(self):
        return '<Comment %r>' % self.content

    @staticmethod
    def comment(replier_id,
                content,
                video_id,
                repliee_id=None,
                time=datetime.datetime.now()):
        _comment = Comment(repliee_id=repliee_id,
                           time=time,
                           content=content,
                           replier_id=replier_id,
                           video_id=video_id)
        db.session.add(_comment)
        db.session.commit()
        return _comment