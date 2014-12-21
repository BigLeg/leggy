from model import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'
    
    MAX_CONTENT_LENGTH = 30
    
    TYPE_FOLLOW = 0
    TYPE_VIDEOCOMMENT = 1
    TYPE_VIDEOSHARE = 2
    
    id = db.Column(db.Integer,primary_key=True)
    userid_from = db.Column(db.Integer, db.ForeignKey('users.id'))
    userid_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Integer,default = TYPE_FOLLOW)
    read = db.Column(db.Boolean,default = False)
    time = db.Column(db.DateTime,default = datetime.utcnow)
    video_id = db.Column(db.Integer,db.ForeignKey('videos.id'),nullable=True,default=None)
    
    related_video = db.relationship('Video')
    
