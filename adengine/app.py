__author__ = "signalpillar"


from . import model
from .config import get_by_name as get_config_by_name

from flask import (
    Flask,
    jsonify,
    make_response,)


def create_app(config_name):

    app = Flask(__name__)

    config = get_config_by_name(config_name)
    app.config.from_object(config)
    config.init_app(app)

    # at this step all the models are
    model.db.init_app(app)
    model.db.app = app

    configure_endpoints(app, model.db)
    # db initialisation should follow endpoints configuration
    # as models metadata is built during previous step
    model.db.create_all()
    return app


def configure_endpoints(app, db=None, session=None):
    """Configure endpoints based on the existing models.

    :param flask.Flask app: Flask Application.
    :param flask.ext.sqlalchemy.SQLAlchemy db: Database configuration.
    :rtype: flask.Flask
    """
    assert db or session

    import flask.ext.restless

    manager = flask.ext.restless.APIManager(app, session=session, flask_sqlalchemy_db=db)

    manager.create_api(model.User, methods=['GET', 'POST', 'DELETE', 'PUT'])
    manager.create_api(model.Ad, methods=['GET', 'POST', 'DELETE', 'PUT'])
    manager.create_api(model.Comment, methods=['GET', 'POST', 'DELETE', 'PUT'])

    return app


def not_found(error):
    return make_response(jsonify({
        "error": "Not found"
    }), 404)
