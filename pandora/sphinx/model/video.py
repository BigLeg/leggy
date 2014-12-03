import os
import datetime
import uuid

from model import db
from model.comment import Comment
from util.video import get_serve_path, get_upload_path

class Video(db.Model):
    __tablename__ = 'videos'

    MAX_TITLE   = 100
    MAX_URL     = 256

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(MAX_TITLE))
    desc            = db.Column(db.Text)
    location        = db.Column(db.String(MAX_URL))
    size            = db.Column(db.Integer)
    play_count      = db.Column(db.Integer, default=0)
    merit           = db.Column(db.Integer, default=0)
    demerit         = db.Column(db.Integer, default=0)
    upload_time     = db.Column(db.DateTime)

    poster_id       = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments        = db.relationship('Comment', backref='video', lazy='dynamic')

    def __repr__(self):
        return '<Video %r>' % self.title

    @staticmethod
    def from_id(id):
        return Video.query.filter_by(id=id).first_or_404()

    @staticmethod
    def upload(file, filename, user):
        upload_path = get_upload_path(filename, user)
        serve_path = get_serve_path(filename, user)

        dir = os.path.dirname(upload_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        file.save(upload_path)

        video = Video(title=filename,
                      location=serve_path,
                      size=os.path.getsize(upload_path),
                      upload_time=datetime.datetime.now(),
                      poster_id=user.id)
        db.session.add(video)
        db.session.commit()
        return video
