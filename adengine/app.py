__author__ = "signalpillar"


import adengine.config as app_config

from flask import (
    Flask,
    jsonify,
    make_response,)


from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)


def create_app(config_name):
    global app
    app.errorhandler(404)(not_found)

    config = app_config.get_by_name(config_name)

    app.config.from_object(config)
    config.init_app(app)

    app = configure_endpoints(app, db)
    # db initialisation should follow endpoints configuration
    # as models metadata is built during previous step
    db.create_all()
    return app


def configure_endpoints(app, db):
    """Configure endpoints based on the existing models.

    :param flask.Flask app: Flask Application.
    :param flask.ext.sqlalchemy.SQLAlchemy db: Database configuration.
    :rtype: flask.Flask
    """
    import flask.ext.restless

    manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

    from .models import user, ad, comment

    manager.create_api(user.User, methods=['GET', 'POST', 'DELETE', 'PUT'])
    manager.create_api(ad.Ad, methods=['GET', 'POST', 'DELETE', 'PUT'])
    manager.create_api(comment.Comment, methods=['GET', 'POST', 'DELETE', 'PUT'])

    return app


def not_found(error):
    return make_response(jsonify({
        "error": "Not found"
    }), 404)
