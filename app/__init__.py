# _*_ coding:utf-8 _*_

from flask import Flask
from config import config
from flask_mail import Mail, Message
from flask_login import LoginManager
from logbook import Logger

from .lib.mysql import MySQLClient
from .lib.redisclient import RedisClient
from .lib.ueditor import UEditor
from .log import setup_logger


mail = Mail()
mysql_client = MySQLClient()
login_manager = LoginManager()
redis_client = RedisClient()
ueditor = UEditor()


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.sign'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    setup_logger(app.config)
    log = Logger("APP")
    log.debug(app.config)

    mail.init_app(app)
    log.debug(mysql_client.init_app(app))
    login_manager.init_app(app)
    log.debug(redis_client.init_app(app))
    ueditor.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
