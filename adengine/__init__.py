from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from adengine.config import config
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # attach routes and custom error pages here
    return app

