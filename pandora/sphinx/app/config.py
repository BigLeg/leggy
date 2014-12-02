import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    CACHE_TYPE = 'simple'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    VIDEOS_UPLOAD_FOLDER = '/data/videos'
    MAIL_SERVER = 'postfix'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('SYS_MAIL_USER') or 'no-reply'
    MAIL_PASSWORD = os.environ.get('SYS_MAIL_PASSWD') or 'passwd'
    LEGGY_MAIL_SUBJECT_PREFIX = '[Mr. Leg]'
    LEGGY_MAIL_SENDER = 'no-reply@leggyleggy.com'
    LEGGY_ADMIN = 'admin'
    LEGGY_POSTS_PER_PAGE = 20
    LEGGY_FOLLOWERS_PER_PAGE = 50
    LEGGY_COMMENTS_PER_PAGE = 30
    LEGGY_SLOW_DB_QUERY_TIME = 0.5
    USE_STUB = False

    @staticmethod
    def init_app(app):
        pass



class DockerConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@mysql/sphinx'

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        app.debug = True



class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/sphinx'

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        app.debug = True



class FrontendConfig(BaseConfig):
    USE_STUB = True
    
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)


    
class TestConfig(BaseConfig):
    TESTING = True
    # TODO: 
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False



class ProdConfig(BaseConfig):
    # TODO:
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.LEGGY_MAIL_SENDER,
            toaddrs=[cls.LEGGY_ADMIN],
            subject=cls.LEGGY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')



configs = {
    'dev-docker':   DockerConfig,
    'dev-local':    LocalConfig,
    'dev-frontend': FrontendConfig,
    'test':         TestConfig,
    'prod':         ProdConfig,
}