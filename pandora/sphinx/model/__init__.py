from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from datetime import datetime   

class SphinxCache(Cache):
    def init_app(self, app):
        super(SphinxCache, self).init_app(
            app=app,
            config={'CACHE_TYPE': app.config['CACHE_TYPE']}
        )

db = SQLAlchemy()
cache = SphinxCache()

follow_table = db.Table('followers',
                db.Column('follower_id',db.Integer,db.ForeignKey('users.id')),
                db.Column('followee_id',db.Integer,db.ForeignKey('users.id')),
                db.Column('timestamp',db.DateTime, default=datetime.utcnow)
            )