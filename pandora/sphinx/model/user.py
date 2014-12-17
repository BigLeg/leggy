import hashlib

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request

from model import db
from model import cache
from model.follow import Follow
from model.video import Video
from model.comment import Comment

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    MAX_USERNAME        = 50
    MAX_EMAIL           = 80
    MAX_PASSWORD        = 128
    MAX_PORTRAIT_PATH   = 150

    ROLE_ADMIN  = 'admin'
    ROLE_NORMAL = 'normal'

    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(MAX_USERNAME), unique=True)
    email           = db.Column(db.String(MAX_EMAIL), unique=True)
    password_hash   = db.Column(db.String(MAX_PASSWORD))
    role            = db.Column(db.Enum(ROLE_ADMIN, ROLE_NORMAL), default=ROLE_NORMAL)
    banned          = db.Column(db.Boolean, default=False)
    confirmed       = db.Column(db.Boolean, default=False)
    portrait_path   = db.Column(db.String(MAX_PORTRAIT_PATH))

    videos          = db.relationship('Video', backref='poster', lazy='dynamic')
    comments        = db.relationship('Comment', backref='replier', foreign_keys=[Comment.replier_id], lazy='dynamic')
    replied         = db.relationship('Comment', backref='repliee', foreign_keys=[Comment.repliee_id], lazy='dynamic')
    followees = db.relationship('Follow',
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followee_id],
                                backref=db.backref('followee', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def from_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def from_username(username):
        return User.query.filter_by(username=username).first()

    # need to check if exists
    @staticmethod
    def create(email, username, password):
        user = User(email=email,
                    username=username,
                    password=password,
                    confirmed=True)  # TODO: allow confirm later
        db.session.add(user)
        db.session.commit()
        return user

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)