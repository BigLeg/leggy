from flask import Flask

from app.config import configs
import conf

conf.load('conf', 'sphinx')
cfg = conf.get_context()
config = configs[cfg.mode]

def create_app(name=__name__, config=config):
    app = Flask(name, template_folder='../templates', static_folder='../static')
    app.config.from_object(config)
    config.init_app(app)
    return app
